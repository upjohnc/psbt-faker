default:
    just --list

run args="":
    python psbt_faker/main.py {{ args }}
