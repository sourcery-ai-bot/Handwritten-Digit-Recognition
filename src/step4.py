import numpy as np
import matplotlib.pyplot as plt


# A function to plot images
def show_image(img):
    image = img.reshape((28, 28))
    plt.imshow(image, 'gray')


def sigmoid(seq):
    return 1 / (1 + np.exp(-seq))


def sigmoid_deriv(seq):
    return sigmoid(seq) * (1 - sigmoid(seq))


def show_cost(step_number, epoch_count, costs):
    plt.title("Step" + str(step_number))
    x = np.arange(0,epoch_count)
    plt.plot(x, costs)
    plt.savefig(f"/Users/amiroo/Desktop/Handwritten-Digit-Recognition/costs/cost{step_number}.png")


# Reading The Train Set
train_images_file = open('/Users/amiroo/Desktop/Handwritten-Digit-Recognition/samples/train-images-idx3-ubyte', 'rb')
train_images_file.seek(4)
num_of_train_images = int.from_bytes(train_images_file.read(4), 'big')
train_images_file.seek(16)

train_labels_file = open('/Users/amiroo/Desktop/Handwritten-Digit-Recognition/samples/train-labels-idx1-ubyte', 'rb')
train_labels_file.seek(8)

train_set = []
for _ in range(num_of_train_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i, 0] = int.from_bytes(train_images_file.read(1), 'big') / 256

    label_value = int.from_bytes(train_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1

    train_set.append((image, label))


# Reading The Test Set
test_images_file = open('/Users/amiroo/Desktop/Handwritten-Digit-Recognition/samples/t10k-images-idx3-ubyte', 'rb')
test_images_file.seek(4)

test_labels_file = open('/Users/amiroo/Desktop/Handwritten-Digit-Recognition/samples/t10k-labels-idx1-ubyte', 'rb')
test_labels_file.seek(8)

num_of_test_images = int.from_bytes(test_images_file.read(4), 'big')
test_images_file.seek(16)

test_set = []
for _ in range(num_of_test_images):
    image = np.zeros((784, 1))
    for i in range(784):
        image[i] = int.from_bytes(test_images_file.read(1), 'big') / 256

    label_value = int.from_bytes(test_labels_file.read(1), 'big')
    label = np.zeros((10, 1))
    label[label_value, 0] = 1

    test_set.append((image, label))


# Fourth step
w1 = np.random.normal(loc=0, scale=1, size=(16, 28*28))
w2 = np.random.normal(loc=0, scale=1, size=(16, 16))
w3 = np.random.normal(loc=0, scale=1, size=(10, 16))

b1 = np.zeros((16,1))
b2 = np.zeros((16,1))
b3 = np.zeros((10,1))

batch_size = 10
learning_rate = 1
count_epoch = 200

costs = []
for i in range(count_epoch):

    accuracy = 0
    cost = 0

    # np.random.shuffle(train_set)
    b_size = int(100 / batch_size)

    for i in range(b_size):
        gw1 = np.zeros((16, 784))
        gw2 = np.zeros((16, 16))
        gw3 = np.zeros((10, 16))
        gb1 = np.zeros((16, 1))
        gb2 = np.zeros((16, 1))
        gb3 = np.zeros((10, 1))
        ga2 = np.zeros((16, 1))
        ga1 = np.zeros((16, 1))

        for r in range(batch_size):
            element_num = i * batch_size + r
            main_mtx = np.asarray(train_set[element_num][0])
            z1 = w1 @ main_mtx + b1
            mtx2 = sigmoid(z1)
            z2 = w2 @ mtx2 + b2
            mtx3 = sigmoid(z2) 
            z3 = w3 @ mtx3 + b3
            f_mtx = sigmoid(z3) 

            cost += sum(pow((f_mtx - train_set[element_num][1]), 2))

            y = train_set[element_num][1]

            gw3 += (2 * (f_mtx - y) * sigmoid_deriv(z3)) @ np.transpose(mtx3)
            gb3 += (2 * (f_mtx - y) * sigmoid_deriv(z3))
            ga2 = np.transpose(w3) @ (2 * (f_mtx - y) * sigmoid_deriv(z3))
            gw2 += (ga2 * sigmoid_deriv(z2)) @ np.transpose(mtx2)
            gb2 += (ga2 * sigmoid_deriv(z2))
            ga1 = np.transpose(w2) @ (ga2 * sigmoid_deriv(z2))
            gw1 += (ga1 * sigmoid_deriv(z1) @ np.transpose(main_mtx))
            gb1 += (ga1 * sigmoid_deriv(z1))

            max_value = np.max(f_mtx)
            index_max_value = np.argmax(f_mtx)

            if train_set[element_num][1][index_max_value] == 1:
                accuracy += 1

        w1 = w1 - (learning_rate * (gw1 / batch_size))
        w2 = w2 - (learning_rate * (gw2 / batch_size))
        w3 = w3 - (learning_rate * (gw3 / batch_size))

        b1 = b1 - (learning_rate * (gb1 / batch_size))
        b2 = b2 - (learning_rate * (gb2 / batch_size))
        b3 = b3 - (learning_rate * (gb3 / batch_size))

    costs.append(cost/100)

print(f"Accuracy is: {accuracy}%")
show_cost(4, count_epoch, costs)
