#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import datetime
import json
import os
import pathlib
import subprocess
import sys
import ffmpeg

logger = logging.getLogger(__name__)

def run_command(command, **kwargs):
    sys.stdout.write(' '.join(command) + '\n')
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, **kwargs)
    while proc.poll() is None:
        msg = proc.stdout.readline()
        if msg:
            sys.stdout.write(msg)    
    return proc.returncode

def resize_video(input_file, output_file, width, height, convert_fps):
    fps_target = 30.0
    probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width_in = int(video_stream['width'])
    height_in = int(video_stream['height'])
    rate = video_stream['r_frame_rate'].split('/')
    fps_in = float(rate[0]) / float(rate[1])
    stream = ffmpeg.input(input_file)
    if width == width_in and height == height_in:
        pass
    else:
        if width / height == width_in / height_in:
            stream = ffmpeg.filter(stream, 'scale', width=width, height=height)
        elif width / height > width_in / height_in:
            w = int(height * width_in / height_in / 2) * 2
            pad_x = int((width - w) / 2)
            stream = ffmpeg.filter(stream, 'scale', width=w, height=height)
            stream = ffmpeg.filter(stream, 'pad', width=width, height=height, x=pad_x, y=0, color='black')
        else:
            h = int(width * height_in / width_in / 2) * 2
            pad_y = int((height - h) / 2)
            stream = ffmpeg.filter(stream, 'scale', width=width, height=h)
            stream = ffmpeg.filter(stream, 'pad', width=width, height=height, x=0, y=pad_y, color='black')

    if convert_fps and fps_in != fps_target:
        stream = ffmpeg.filter(stream, 'framerate', fps=fps_target)

    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream, overwrite_output=True)

def estimate_pose2d(input_video, output_json_dir, pose2d_video, conf):
    # tf-pose-estimation
    tfpose_args = [sys.executable, 'run_video.py',
                '--video', str(input_video),
                '--model', 'mobilenet_v2_large',
                '--write_json', str(output_json_dir),
                '--number_people_max', str(conf['max_people']),
                '--frame_first', str(conf['first_frame']),
                '--write_video', str(pose2d_video),
                '--no_display']
    if conf['no_bg']:
        tfpose_args.append('--no_bg')
    logger.debug('tfpose_args:' + str(tfpose_args))
    return run_command(tfpose_args, cwd=conf['tfpose_dir'])

def estimate_depth(input_video, output_json_dir, dttm, conf):
    # mannequinchallenge-vmd
    depth_args = [sys.executable, 'predict_video.py',
                '--video_path', str(input_video),
                '--json_path', str(output_json_dir),
                '--interval',  '20',
                '--reverse_specific', conf['reverse_list'],
                '--order_specific', conf['order_list'],
                '--avi_output', 'yes',
                '--verbose',  str(conf['log_level']),
                '--number_people_max', str(conf['max_people']),
                '--end_frame_no', str(conf['last_frame']),
                '--now', dttm,
                '--input', 'single_view',
                '--batchSize', '1',
                '--order_start_frame', str(conf['order_start_frame'])]
    logger.debug('depth_args:' + str(depth_args))
    return run_command(depth_args, cwd=conf['depth_dir'])

def estimate_pose3d(output_sub_dir, conf):
    # 3d-pose-baseline-vmd
    pose3d_args = [sys.executable, 'src/openpose_3dpose_sandbox_vmd.py',
                  '--camera_frame', '--residual', '--batch_norm',
                  '--dropout', '0.5',
                  '--max_norm', '--evaluateActionWise', '--use_sh',
                  '--epochs', '200',
                  '--load', '4874200',
                  '--gif_fps', '30',
                  '--verbose', str(conf['log_level']),
                  '--openpose', str(output_sub_dir),
                   '--person_idx', '1']
    if conf['add_leg']:
        pose3d_args.append('--add_leg')
    logger.debug('pose3d_args:' + str(pose3d_args))
    return run_command(pose3d_args, cwd=conf['pose3d_dir'])

def pose3d_to_vmd(output_sub_dir, conf):
    # VMD-3d-pose-baseline-multi
    vmd3d_args = [sys.executable, 'main.py',
                  '-v', '2',
                  '-t', str(output_sub_dir),
                  '-b', conf['vmd3d_bone_csv'] if 'vmd3d_bone_csv' in conf else 'born/animasa_miku_born.csv',
                  '-c', '30',
                  '-z', '1.5',
                  '-s', '1',
                  '-p', '0.5',
                  '-r', '5',
                  '-k', '1',
                  '-e', '0',
                  '-d', '4']
    logger.debug('vmd3d_args:' + str(vmd3d_args))
    return run_command(vmd3d_args, cwd=conf['vmd3d_dir'])

def add_face_motion(input_video, output_json_dir, input_video_filename, dttm, conf):
    rfv_output_dir = pathlib.Path(str(output_json_dir) + '_' + dttm + '_idx01')
    face_vmd_file = rfv_output_dir / (input_video_filename + '-face.vmd')
    rfv_args = ['./readfacevmd',
                str(input_video), str(face_vmd_file)]
    if 'rfv_nameconf' in conf:
        rfv_args.extend(['--nameconf', conf['rfv_nameconf']])
    logger.debug('rfv_args:' + str(rfv_args))
    ret = run_command(rfv_args, cwd=conf['rfv_dir'])
    if ret != 0:
        return ret, None

    body_vmd_file = list(rfv_output_dir.glob('**/*_reduce.vmd'))[0].resolve()
    merged_vmd_file = rfv_output_dir / (input_video_filename + '-merged.vmd')
    merge_args = ['./mergevmd', str(body_vmd_file), str(face_vmd_file), str(merged_vmd_file)]
    logger.debug('merge_args:' + str(merge_args))
    ret = run_command(merge_args, cwd=conf['rfv_dir'])
    return ret, merged_vmd_file

def resize_motion(src_vmd_file, trace_pmx, replace_pmx, conf):
    sizing_args = [sys.executable, 'src/main.py',
                   '--vmd_path', str(src_vmd_file),
                   '--trace_pmx_path', trace_pmx,
                   '--replace_pmx_path', replace_pmx,
                   '--avoidance', '1',
                   '--hand_ik', '1',
                   '--hand_distance', '1.7',
                   '--verbose', str(conf['log_level'])]
    logger.debug('sizing_args:' + str(sizing_args))
    return run_command(sizing_args, cwd=conf['sizing_dir'])

def autotracevmd(conf):
    input_video = pathlib.Path(conf['VIDEO_FILE']).resolve()
    input_video_dir = input_video.parent
    input_video_filename = input_video.stem
    output_dir = input_video_dir
    if conf['output_dir'] != '':
        output_dir = pathlib.Path(conf['output_dir']).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    dttm = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_json_dir = output_dir / (input_video_filename + '_' + dttm) / (input_video_filename + '_json')
    output_json_dir.mkdir(parents=True, exist_ok=True)
    pose2d_video = output_dir / (input_video_filename + '_' + dttm) / (input_video_filename + '_openpose.avi')
    modified_video = output_dir / (input_video_filename + '_' + dttm) / (input_video_filename + '_modified.mp4')
    if conf['resize'] or conf['convert_fps']:
        width = conf['resize_width']
        height = conf['resize_height']
        resize_video(str(input_video), str(modified_video), width, height, conf['convert_fps'])
    else:
        modified_video = input_video

    ret = estimate_pose2d(modified_video, output_json_dir, pose2d_video, conf)
    if ret != 0:
        return '2D pose estimation error', None

    # update dttm
    dttm = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    ret = estimate_depth(modified_video, output_json_dir, dttm, conf)
    if ret != 0:
        return 'depth estimation error', None

    for idx in range(1, conf['max_people'] + 1):
        output_sub_dir = pathlib.Path(str(output_json_dir) + '_' + dttm + '_idx0' + str(idx))
        ret = estimate_pose3d(output_sub_dir, conf)
        if ret != 0:
            return '3D pose estimation error', None
        ret = pose3d_to_vmd(output_sub_dir, conf)
        if ret != 0:
            return '3D pose -> VMD error', None

    if 'rfv_enable' in conf and conf['rfv_enable']:
        ret, sizing_src_vmd = add_face_motion(modified_video, output_json_dir, input_video_filename, dttm, conf)
        if ret != 0:
            return 'readfacevmd error', None
    else:
        vmd_output_dir = pathlib.Path(str(output_json_dir) + '_' + dttm + '_idx01')
        sizing_src_vmd = list(vmd_output_dir.glob('**/*_reduce.vmd'))[0].resolve()

    if 'sizing_trace_pmx' in conf and 'sizing_replace_pmx_list' in conf:
      for replace_pmx in conf['sizing_replace_pmx_list']:
            ret = resize_motion(sizing_src_vmd, conf['sizing_trace_pmx'], replace_pmx, conf)
            if ret != 0:
                return 'sizing error', None
    return None, vmd_output_dir

if __name__ == '__main__':
    config_file = pathlib.Path('config.json')
    if config_file.is_file():
        with config_file.open() as fconf:
            conf = json.load(fconf)
    else:
        conf = {}
    parser = argparse.ArgumentParser(description='estimate human pose from movie and generate VMD motion')
    parser.add_argument('--output_dir', action='store', type=str, default=conf['output_dir'] if 'output_dir' in conf else '', help='output directory')
    parser.add_argument('--log_level', action='store', type=int, default=conf['log_level'] if 'log_level' in conf else 1, help='log verbosity')
    parser.add_argument('--first_frame', action='store', type=int, default=conf['first_frame'] if 'first_frame' in conf else 0, help='first frame to analyze')
    parser.add_argument('--last_frame', action='store', type=int, default=conf['last_frame'] if 'last_frame' in conf else -1, help='last frame to analyze')
    parser.add_argument('--max_people', action='store', type=int, default=conf['max_people'] if 'max_people' in conf else 1, help='maximum number of people to analyze')
    parser.add_argument('--reverse_list', action='store', type=str, default=conf['reverse_list'] if 'reverse_list' in conf else '', help='list to specify reversed person')
    parser.add_argument('--order_list', action='store', type=str, default=conf['order_list'] if 'order_list' in conf else '', help='list to specify person index in left-to-right order')
    parser.add_argument('--order_start_frame', action='store', type=int, default=conf['order_start_frame'] if 'order_start_frame' in conf else 0, help='order_start_frame')
    parser.add_argument('--add_leg', action='store_true', default=conf['add_leg'] if 'add_leg' in conf else False, help='add invisible legs to estimated joints')
    parser.add_argument('--no_bg', action='store_true', default=conf['no_bg'] if 'no_bg' in conf else False, help='disable BG output (show skeleton only)')
    parser.add_argument('VIDEO_FILE')
    arg = parser.parse_args()
    argdic = vars(arg)
    for k in argdic.keys():
        conf[k] = argdic[k]

    if conf['log_level'] == 0:
        logger.setLevel(logging.ERROR)
    elif conf['log_level'] == 1:
        logger.setLevel(logging.WARNING)
    elif conf['log_level'] == 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    autotracevmd(conf)
