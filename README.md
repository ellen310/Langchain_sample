# Langchain을 활용한 기본 RAG 구현 예시
여러 형식의 문서를 로드, 확장자 별 컬렉션 생성(선택), 임베딩 후 저장 및 검색

## - Vector Store
Qdrant <br/>
https://qdrant.tech/documentation/guides/installation/
<br/>
https://artifacthub.io/packages/helm/qdrant/qdrant
<br/><br/>

- K8s
```
k create -n qdrant

helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm repo update
helm upgrade -i qdrant -n qdrant qdrant/qdrant #install

k get all -n qdrant
```
<br/>

NodePort svc로 변경 (테스트 용도)
```
helm upgrade -i qdrant qdrant/qdrant \
  --set service.type=NodePort \
  --namespace qdrant
```
<br/>

- Docker
```
docker run -p 6333:6333 -d qdrant/qdrant
```

## - 설치 시 참고사항 (문서 발췌)
If you want to run Qdrant in your own infrastructure, without any cloud connection, we recommend to install Qdrant in a Kubernetes cluster with our Qdrant Private Cloud Enterprise Operator. <br/>
For testing or development setups, you can run the Qdrant container or as a binary executable. We also provide a Helm chart for an easy installation in Kubernetes.

