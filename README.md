# Занятие 4. Работа с GIT.
## Симулятор системы управления мотором.
### Описание:
 1. **motor_control_module**  - модуль содержит реализации следующих классов: PI_Regulator (пропорциоально-интегральный регулятор), FeedbackFilter( БИХ фильтр нижних частот ).

 2. **motor_control.py** - тестовое приложение, в котором осуществляется моделирование объекта управления, замкнутого в цепь обратной связи через ПИ-регулятор. В качестве объекта управления моделируется простое звено первого порядка. В цепь обратной связи добавлен шум.

 3. **config,yaml** - параметры приложения:
```yaml
 general_params:
  T_stop: 20                # Modelling time(s)
  sampling_frequency: 100   # Sampling frequency(Hz)
regulator_params:
  Kp: 8.0                   # Proportional gain
  Ki: 0.03                  # Integral gain
  max_action: 48.0          # Max. output of regulator(Volts)
  min_action: -48.0         # Min. output of regulator(Volts)
imitation_model_params:     
  Noise_amplitude: 0.01     # Amplitude of gauss noise in feedback loop
  Gain: 0.5                 # Decay factor of exponent
  Initial_cond: 0.0         # Initial condition
feedback_filter_params:
  pass_frequency: 2.5       # Feedback filter pass frequency(Hz)
  

 ```
 ### Запуск приложения.

 1. Клонирование репозитория:

    ```bash
    git clone git@github.com:vorobyevd/linux_for_robotics_lesson4.git
    ```
2. Переход в папку проекта.
    ```bash
    cd linux_for_robotics_lesson4/
    ```
3. Обновление репозитория:

    ```bash
    git pull origin main
    ```
   
4. Проверка зависимостей:
    ```make
    make install
    ```
5. Запуск приложения:
    ```bash
    make run
    ```
    Вывод приложения:

    ![Application output](/assets/Output.png)

 