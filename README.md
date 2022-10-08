# Polyglot api

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/jason9693/polyglot-deploy)

한국어 혐오성 게시글 분류모델.

### How to use

    curl -X POST "https://polyglot-deploy-jason9693.endpoint.ainize.ai/generate" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=제정신이냐?"

### Post parameter

    text: prompt gives to model.


## * With CLI *

### Types: logits (confidence rate)

#### Input example

    curl -X POST "https://master-soongsil-bert-base-beep-deploy-jason9693.endpoint.ainize.ai/predict/logits" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=제정신이냐?"
    

### Types: class

#### Input example

    curl -X POST "https://master-soongsil-bert-base-beep-deploy-jason9693.endpoint.ainize.ai/predict/class" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=제정신이냐?"

#### Output example


    {
        "dpstring": "공격발언",
        "result": "1"
    }

