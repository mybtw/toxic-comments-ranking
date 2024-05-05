#!/bin/bash

# Задайте значения по умолчанию, если переменные окружения не установлены
: ${HOST:='0.0.0.0'}
: ${PORT:='5000'}
: ${WORKERS:='4'}
: ${THREADS:='2'}

# Запустите приложение с помощью Gunicorn
exec gunicorn -b $HOST:$PORT -w $WORKERS --threads $THREADS main:app