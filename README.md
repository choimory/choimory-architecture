# choimory-io-architect

- choimory-io 구조를 diagrams(https://diagrams.mingrammer.com)코드로 작성

# set up

```shell
# python3
brew install python
python3 --version

# grapviz, 다이어그램 그리는 툴
brew install graphviz
dot -V
```

- brew

```shell
python3 -m venv venv
source venv/bin/activate
pip install diagrams
touch choimory-io-architect.py
```

- 프로젝트 안에서 파이썬 가상환경 설정

# 시작

`source venv/bin/activate`

# 이미지 생성

`python3 choimory-io-architect.py`

# 종료

`deactivate`