default:
    just --list

run *args="":
    PYTHONPATH=. python psbt_faker/main.py {{ args }}
