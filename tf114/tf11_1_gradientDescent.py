import tensorflow as tf
import matplotlib.pyplot as plt
tf.set_random_seed(123)


x_train = 1
y_train = 1
x = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)

# w = tf.compat.v1.Variable(tf.compat.v1.random_normal([10]), name="weight")
w = tf.compat.v1.Variable([10], dtype=tf.float32, name="weight")

hypothesis = x * w

loss = tf.reduce_mean(tf.square(hypothesis -y))


lr = 0.1   # lr === learning_rate
gradient = tf.reduce_mean((w * x - y ) * x)
descent  = w - lr * gradient
update = w.assign(descent)

w_history = []
loss_history = []

sess  = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

for step in range(10):
    
    _, loss_v , w_val = sess.run([update, loss, w], feed_dict={x:x_train, y:y_train})
    print(step, '\t' , loss_v, '\t', w_val)
    
    w_history.append(w_val)
    loss_history.append(loss_v)
    
sess.close()

print("=============================w history=============================")
print(w_history)
print("=============================loss history=============================")
print(loss_history)

# plt.plot(w_history, loss_history)
# plt.xlabel("weight")
# plt.ylabel("loss")
# plt.show()


# 0        81.0    [9.1]
# 1        65.61001        [8.29]