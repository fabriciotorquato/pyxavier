# Pyxavier

## Requirements

- [Git](https://git-scm.com/downloads)
- [Virtualvenv](https://virtualenv.pypa.io/en/latest/)

## Library

### Python

| Description        | Tech   | Resources                                |
| ------------------ | ------ | ---------------------------------------- |
| get raw data - EEG | Emokit | [API](https://github.com/openyou/emokit) |

### Setup project

    ./setup.sh

### Run

    source venv/bin/activate

    python -m example.create_dataset --dir={bci/emotion/ihc} --full={True/False}

    python -m example.training_model --dir={bci/emotion/ihc} --show={True/False} --full={True/False}

    python -m example.run_mlp --dir={bci/emotion/ihc} --show={True/False} --full={True/False}

    python -m example.run_cnn --dir={bci/emotion/ihc} --show={True/False} --full={True/False}

    python -m example.run_rnn --dir={bci/emotion/ihc} --show={True/False} --full={True/False}
 

