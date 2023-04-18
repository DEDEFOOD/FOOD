import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, LSTM, SimpleRNN

# time step만큼 시퀀스 데이터 분리
def split_sequence(sequence, step):
    x, y = list(), list()

    for i in range(len(sequence)):
        end_idx = i + step
        if end_idx > len(sequence) - 1:
            break

        seq_x, seq_y = sequence[i:end_idx], sequence[end_idx]
        x.append(seq_x)
        y.append(seq_y)

    return np.array(x), np.array(y)


# sin 함수 학습 데이터
x = [i for i in np.arange(start=-10, stop=10, step=0.1)]
train_y = [np.sin(i) for i in x]
# 학습 데이터셋 저장


# 하이퍼파라미터
n_timesteps = 15
n_features = 1
# 입력 시퀀스 길이를 15로 정의, 입력 벡터의 크기 1로 정의


# 시퀀스 나누기
# train_x.shape => (samples, timesteps)
# train_y.shape => (samples)
train_x, train_y = split_sequence(train_y, step=n_timesteps)
print("shape x:{} / y:{}".format(train_x.shape, train_y.shape))
# 학습데이터 셋을 입력 시퀀스 길이만큼 나눠 입력 시퀀스 생성



# RNN 입력 벡터 크기를 맞추기 위해 벡터 차원 크기 변경
# reshape from [samples, timesteps] into [samples, timesteps, features]
train_x = train_x.reshape(train_x.shape[0], train_x.shape[1], n_features)
print("train_x.shape = {}".format(train_x.shape))
print("train_y.shape = {}".format(train_y.shape))
# 2차원 x모델을 3차원 형태로 변환



# RNN 모델 정의
model = Sequential()
model.add(SimpleRNN(units=10, return_sequences=False, input_shape=(n_timesteps, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
# RNN계층정의 후 모델 생성
# simple RNN 계층
# 입력 데이터 형상 정의
# 손실함수 mse
# 옵티마이저 adam



# 모델 학습
np.random.seed(0)
from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=5, mode='auto')
history = model.fit(train_x, train_y, epochs=1000, callbacks=[early_stopping])
# 모델 학습
# 조기종료 함수 설정(급격히 손실이 증가하면)


# loss 그래프 생성
plt.plot(history.history['loss'], label="loss")
plt.legend(loc="upper right")
plt.show()


# 테스트 데이터셋 생성
test_x = np.arange(10, 20, 0.1)
calc_y = np.cos(test_x) # 테스트 정답 데이터
# RNN모델을 테스트 하기위해
# cos()를 이용하여 원본 데이터에 주기적 차이를 준다


# RNN 모델 예측 및 로그 저장
test_y = calc_y[:n_timesteps]
for i in range(len(test_x) - n_timesteps):
    net_input = test_y[i : i + n_timesteps]
    net_input = net_input.reshape((1, n_timesteps, n_features))
    train_y = model.predict(net_input, verbose=0)
    print(test_y.shape, train_y.shape, i, i + n_timesteps)
    test_y = np.append(test_y, train_y)
# 예측값을 저장



# 예측 결과 그래프 그리기
plt.plot(test_x, calc_y, label="ground truth", color="orange")
plt.plot(test_x, test_y, label="predicitons", color="blue")
plt.legend(loc='upper left')
plt.ylim(-2, 2)
plt.show()
# 출력
# 오차가 거의 없다

'''
shape x:(185, 15) / y:(185,)
train_x.shape = (185, 15, 1)
train_y.shape = (185,)   
Epoch 1/1000
6/6 [==============================] - 1s 5ms/step - loss: 1.2445
Epoch 2/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.0956
Epoch 3/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.9475
Epoch 4/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.8164
Epoch 5/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.6899
Epoch 6/1000
6/6 [==============================] - 0s 6ms/step - loss: 0.5678
Epoch 7/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.4551
Epoch 8/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.3510
Epoch 9/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.2482
Epoch 10/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.1595
Epoch 11/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0987
Epoch 12/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0717
Epoch 13/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0563
Epoch 14/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0462
Epoch 15/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0414
Epoch 16/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0401
Epoch 17/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0382
Epoch 18/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0359
Epoch 19/1000
6/6 [==============================] - 0s 10ms/step - loss: 0.0339
Epoch 20/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0322
Epoch 21/1000
6/6 [==============================] - 0s 8ms/step - loss: 0.0305
Epoch 22/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0290
Epoch 23/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0275
Epoch 24/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0263
Epoch 25/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0248
Epoch 26/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0234
Epoch 27/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0220
Epoch 28/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0207
Epoch 29/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0194
Epoch 30/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0181
Epoch 31/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0169
Epoch 32/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0158
Epoch 33/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0148
Epoch 34/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0138
Epoch 35/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0129
Epoch 36/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0122
Epoch 37/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0115
Epoch 38/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0108
Epoch 39/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0102
Epoch 40/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0097
Epoch 41/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0091
Epoch 42/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0087
Epoch 43/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0082
Epoch 44/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0078
Epoch 45/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0074
Epoch 46/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0070
Epoch 47/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0067
Epoch 48/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0063
Epoch 49/1000
6/6 [==============================] - 0s 6ms/step - loss: 0.0060
Epoch 50/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0057
Epoch 51/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0054
Epoch 52/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0051
Epoch 53/1000
6/6 [==============================] - 0s 7ms/step - loss: 0.0049
Epoch 54/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0046
Epoch 55/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0044
Epoch 56/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0042
Epoch 57/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0040
Epoch 58/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0038
Epoch 59/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0036
Epoch 60/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0035
Epoch 61/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0033
Epoch 62/1000
6/6 [==============================] - 0s 5ms/step - loss: 0.0032
Epoch 63/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0031
Epoch 64/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0030
Epoch 65/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0029
Epoch 66/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0028
Epoch 67/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0027
Epoch 68/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0027
Epoch 69/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0026
Epoch 70/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0025
Epoch 71/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0024
Epoch 72/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0024
Epoch 73/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0023
Epoch 74/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0023
Epoch 75/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0022
Epoch 76/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0021
Epoch 77/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0021
Epoch 78/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0020
Epoch 79/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0020
Epoch 80/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0019
Epoch 81/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0018
Epoch 82/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0018
Epoch 83/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0017
Epoch 84/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0017
Epoch 85/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0016
Epoch 86/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0016
Epoch 87/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0015
Epoch 88/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0015
Epoch 89/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0014
Epoch 90/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0013
Epoch 91/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0013
Epoch 92/1000
6/6 [==============================] - 0s 6ms/step - loss: 0.0013
Epoch 93/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0012
Epoch 94/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0012
Epoch 95/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0011
Epoch 96/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0011
Epoch 97/1000
6/6 [==============================] - 0s 4ms/step - loss: 0.0010
Epoch 98/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.9651e-04
Epoch 99/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.1934e-04
Epoch 100/1000
6/6 [==============================] - 0s 5ms/step - loss: 8.9005e-04
Epoch 101/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.3025e-04
Epoch 102/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.0504e-04
Epoch 103/1000
6/6 [==============================] - 0s 4ms/step - loss: 7.6551e-04
Epoch 104/1000
6/6 [==============================] - 0s 5ms/step - loss: 7.2314e-04
Epoch 105/1000
6/6 [==============================] - 0s 5ms/step - loss: 6.9358e-04
Epoch 106/1000
6/6 [==============================] - 0s 4ms/step - loss: 6.5513e-04
Epoch 107/1000
6/6 [==============================] - 0s 4ms/step - loss: 6.3130e-04
Epoch 108/1000
6/6 [==============================] - 0s 4ms/step - loss: 5.8433e-04
Epoch 109/1000
6/6 [==============================] - 0s 5ms/step - loss: 5.6337e-04
Epoch 110/1000
6/6 [==============================] - 0s 4ms/step - loss: 5.2406e-04
Epoch 111/1000
6/6 [==============================] - 0s 5ms/step - loss: 4.9944e-04
Epoch 112/1000
6/6 [==============================] - 0s 5ms/step - loss: 4.7815e-04
Epoch 113/1000
6/6 [==============================] - 0s 4ms/step - loss: 4.4408e-04
Epoch 114/1000
6/6 [==============================] - 0s 5ms/step - loss: 4.3626e-04
Epoch 115/1000
6/6 [==============================] - 0s 5ms/step - loss: 4.0954e-04
Epoch 116/1000
6/6 [==============================] - 0s 4ms/step - loss: 3.8708e-04
Epoch 117/1000
6/6 [==============================] - 0s 4ms/step - loss: 3.6375e-04
Epoch 118/1000
6/6 [==============================] - 0s 4ms/step - loss: 3.3598e-04
Epoch 119/1000
6/6 [==============================] - 0s 5ms/step - loss: 3.2911e-04
Epoch 120/1000
6/6 [==============================] - 0s 4ms/step - loss: 3.1256e-04
Epoch 121/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.8675e-04
Epoch 122/1000
6/6 [==============================] - 0s 5ms/step - loss: 2.7720e-04
Epoch 123/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.5858e-04
Epoch 124/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.4916e-04
Epoch 125/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.3573e-04
Epoch 126/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.2685e-04
Epoch 127/1000
6/6 [==============================] - 0s 5ms/step - loss: 2.2212e-04
Epoch 128/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.0426e-04
Epoch 129/1000
6/6 [==============================] - 0s 4ms/step - loss: 2.0374e-04
Epoch 130/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.9004e-04
Epoch 131/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.8254e-04
Epoch 132/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.7706e-04
Epoch 133/1000
6/6 [==============================] - 0s 6ms/step - loss: 1.7034e-04
Epoch 134/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.6394e-04
Epoch 135/1000
6/6 [==============================] - 0s 6ms/step - loss: 1.6130e-04
Epoch 136/1000
6/6 [==============================] - 0s 6ms/step - loss: 1.7131e-04
Epoch 137/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.5579e-04
Epoch 138/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.5216e-04
Epoch 139/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.4721e-04
Epoch 140/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.4095e-04
Epoch 141/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.4025e-04
Epoch 142/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3371e-04
Epoch 143/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3233e-04
Epoch 144/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3316e-04
Epoch 145/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.3080e-04
Epoch 146/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3411e-04
Epoch 147/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3006e-04
Epoch 148/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3797e-04
Epoch 149/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.3410e-04
Epoch 150/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.2930e-04
Epoch 151/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.1562e-04
Epoch 152/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.1803e-04
Epoch 153/1000
6/6 [==============================] - 0s 8ms/step - loss: 1.1362e-04
Epoch 154/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.1225e-04
Epoch 155/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.1197e-04
Epoch 156/1000
6/6 [==============================] - 0s 7ms/step - loss: 1.0838e-04
Epoch 157/1000
6/6 [==============================] - 0s 8ms/step - loss: 1.0843e-04
Epoch 158/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.0893e-04
Epoch 159/1000
6/6 [==============================] - 0s 7ms/step - loss: 1.0581e-04
Epoch 160/1000
6/6 [==============================] - 0s 7ms/step - loss: 1.0425e-04
Epoch 161/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.0566e-04
Epoch 162/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.0146e-04
Epoch 163/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.0182e-04
Epoch 164/1000
6/6 [==============================] - 0s 5ms/step - loss: 1.0220e-04
Epoch 165/1000
6/6 [==============================] - 0s 6ms/step - loss: 1.0094e-04
Epoch 166/1000
6/6 [==============================] - 0s 5ms/step - loss: 9.8909e-05
Epoch 167/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.7636e-05
Epoch 168/1000
6/6 [==============================] - 0s 6ms/step - loss: 9.8440e-05
Epoch 169/1000
6/6 [==============================] - 0s 5ms/step - loss: 9.9679e-05
Epoch 170/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.9304e-05
Epoch 171/1000
6/6 [==============================] - 0s 4ms/step - loss: 1.0120e-04
Epoch 172/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.4001e-05
Epoch 173/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.1269e-05
Epoch 174/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.7990e-05
Epoch 175/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.8627e-05
Epoch 176/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.6591e-05
Epoch 177/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.6512e-05
Epoch 178/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.4598e-05
Epoch 179/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.7093e-05
Epoch 180/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.7915e-05
Epoch 181/1000
6/6 [==============================] - 0s 4ms/step - loss: 8.6497e-05
Epoch 182/1000
6/6 [==============================] - 0s 4ms/step - loss: 9.0438e-05
Epoch 183/1000
6/6 [==============================] - 0s 5ms/step - loss: 9.0861e-05
(15,) (1, 1) 0 15
(16,) (1, 1) 1 16
(17,) (1, 1) 2 17
(18,) (1, 1) 3 18
(19,) (1, 1) 4 19
(20,) (1, 1) 5 20
(21,) (1, 1) 6 21
(22,) (1, 1) 7 22
(23,) (1, 1) 8 23
(24,) (1, 1) 9 24
(25,) (1, 1) 10 25
(26,) (1, 1) 11 26
(27,) (1, 1) 12 27
(28,) (1, 1) 13 28
(29,) (1, 1) 14 29
(30,) (1, 1) 15 30
(31,) (1, 1) 16 31
(32,) (1, 1) 17 32
(33,) (1, 1) 18 33
(34,) (1, 1) 19 34
(35,) (1, 1) 20 35
(36,) (1, 1) 21 36
(37,) (1, 1) 22 37
(38,) (1, 1) 23 38
(39,) (1, 1) 24 39
(40,) (1, 1) 25 40
(41,) (1, 1) 26 41
(42,) (1, 1) 27 42
(43,) (1, 1) 28 43
(44,) (1, 1) 29 44
(45,) (1, 1) 30 45
(46,) (1, 1) 31 46
(47,) (1, 1) 32 47
(48,) (1, 1) 33 48
(49,) (1, 1) 34 49
(50,) (1, 1) 35 50
(51,) (1, 1) 36 51
(52,) (1, 1) 37 52
(53,) (1, 1) 38 53
(54,) (1, 1) 39 54
(55,) (1, 1) 40 55
(56,) (1, 1) 41 56
(57,) (1, 1) 42 57
(58,) (1, 1) 43 58
(59,) (1, 1) 44 59
(60,) (1, 1) 45 60
(61,) (1, 1) 46 61
(62,) (1, 1) 47 62
(63,) (1, 1) 48 63
(64,) (1, 1) 49 64
(65,) (1, 1) 50 65
(66,) (1, 1) 51 66
(67,) (1, 1) 52 67
(68,) (1, 1) 53 68
(69,) (1, 1) 54 69
(70,) (1, 1) 55 70
(71,) (1, 1) 56 71
(72,) (1, 1) 57 72
(73,) (1, 1) 58 73
(74,) (1, 1) 59 74
(75,) (1, 1) 60 75
(76,) (1, 1) 61 76
(77,) (1, 1) 62 77
(78,) (1, 1) 63 78
(79,) (1, 1) 64 79
(80,) (1, 1) 65 80
(81,) (1, 1) 66 81
(82,) (1, 1) 67 82
(83,) (1, 1) 68 83
(84,) (1, 1) 69 84
(85,) (1, 1) 70 85
(86,) (1, 1) 71 86
(87,) (1, 1) 72 87
(88,) (1, 1) 73 88
(89,) (1, 1) 74 89
(90,) (1, 1) 75 90
(91,) (1, 1) 76 91
(92,) (1, 1) 77 92
(93,) (1, 1) 78 93
(94,) (1, 1) 79 94
(95,) (1, 1) 80 95
(96,) (1, 1) 81 96
(97,) (1, 1) 82 97
(98,) (1, 1) 83 98
(99,) (1, 1) 84 99



'''