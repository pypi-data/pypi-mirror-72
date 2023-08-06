================
russian-numerals
================

Пакет Python для работы с количественными числительными русского языка.

Установка
---------

.. code-block:: shell

    pip install russian-numerals
    # or
    pip install git+https://gitlab.com/djbaldey/russian-numerals.git@master#egg=russian-numerals


Использование в консоли
-----------------------

.. code-block:: shell

    russian-numerals "1234567890"
    russian-numerals --handler=tons "1234567890.123456"
    russian-numerals "восемь девятьсот двадцать четыре шестьсот сорок четыре девяносто девять сорок четыре"
    russian-numerals --help


Использование в коде Python
---------------------------

.. code-block:: python

    from russian_numerals import prepare

    print(prepare("1234567890"))
    print(prepare("1234567890.123456", "tons"))
    print(prepare("восемь девятьсот двадцать четыре шестьсот сорок четыре девяносто девять сорок четыре"))

