import sys
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
print(tf.add(1, 2))

if (tf.test.is_gpu_available()):
    print('Tensorflow is working. GPU is available')
else:
    print('Tensorflow is working. GPU is not available')

sys.exit(0)
