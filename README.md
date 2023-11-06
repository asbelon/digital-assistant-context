# Контекст

В ходе взаимодействия цифрового помощника с пользователем
исполнение [сценария](https://github.com/asbelon/digital-assistant-script) в каждом определенном моменте находится на 
определенном акте. Нахождение исполнения сценария на определенном акте назовем состоянием исполнения сценария. 
Состояние исполнения сценария хранит исполнитель сценария для каждого отдельного пользователя. Состояние 
определяется текущим актом и контекстом. Под контекстом понимается совокупность значений переменных сценария.

Переменные сценария бывают пользовательские и зарезервированные. Пользовательские переменные используются в шаблонах
сообщений, условных сообщениях, вариантах выбора и при присвоении значения.

## Имя переменной

Имя пользовательской переменной имеет специальную структуру и ограничения. Имя переменной может состоять из букв, 
цифр, символа нижнего подчеркивания и символов квадратных скобок, которые допустимо использовать только особым 
образом (см ниже Нотация квадратных скобок).

Переменные принимают значения стокового типа данных. За счет нотации квадратных скобок переменные можно 
организовать в структуры типа ключ-значение.

## Нотация квадратных скобок

Переменные, имя которых задано нотацией квадратных скобок, можно использовать как одну переменную списка. Списки могут
быть именованные и нумерованные.

### Именованные списки

Именованные списки формируются через указание свойства в квадратных скобках.

После основного имени переменной в квадратных скобках указывается имя свойства переменной. Например,
Переменная[Свойство]. При этом ограничение на имя свойства такое же как и для имени простой переменной.

Вложенность свойств может быть произвольной. Например, Переменная[Свойство][ЕщеОдноСвойство].

Если две и более переменных имеют одинаковую часть имени до закрывающейся квадратной скобки, то эти переменные можно
использовать как список. Например, если заданы две переменные Переменная[Свойство][ОдноСвойство]
и Переменная[Свойство][ДругоеСвойство], то можно использовать список $Переменная[Свойство] как переменную в итерациях

### Нумерованные списки

Нумерованные списки задаются через указание пустых квадратных скобок

Переменная[]
Переменная[]

что эквивалентно

Переменная[1]
Переменная[2]

Нумерованные переменные могут быть использованы только как список.