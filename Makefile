.PHONY: run cluster up hello-world install-requirements run-math build-math-docker run-math-docker math-workflow clean-k3d run-go-client

run:
	go run main.go

clean-k3d:
	k3d cluster delete argoagent-cluster || true
	k3d registry delete k3d-registry.localhost || true
	docker stop k3d-registry.localhost || true
	docker rm k3d-registry.localhost || true

cluster: clean-k3d
	k3d registry create k3d-registry.localhost --port 5000 || true
	k3d cluster create argoagent-cluster \
		--api-port 6443 \
		--servers 1 \
		--agents 1 \
		--registry-use k3d-registry.localhost:5000 \
		--wait \
		-p "2746:32746@server:0"
	./install_argo.sh
	kubectl patch service argo-server -n argo --patch '{"spec": {"type": "NodePort", "ports": [{"name": "web", "port": 2746, "targetPort": 2746, "nodePort": 32746}]}}'
	echo "Argo server is available at https://localhost:2746"
	./push_secrets.sh

up: cluster
	@echo "Cluster created, starting application..."
	$(MAKE) run

hello-world:
	argo submit -n argo --watch hello-world.yaml

install-requirements:
	pip install --break-system-packages -r requirements.txt

run-math:
	python3 tools/calc/math_service.py

build-math-docker:
	docker build -f Dockerfile.math_service -t k3d-registry.localhost:5000/math_service:latest .
	docker push k3d-registry.localhost:5000/math_service:latest
	k3d image import k3d-registry.localhost:5000/math_service:latest -c argoagent-cluster

run-math-docker: build-math-docker
	docker run -p 8000:8000 k3d-registry.localhost:5000/math_service:latest python3 ./math_cli.py "3*3"

math-workflow:
	argo submit -n argo --watch argo-math-service.yaml -p expression="5*5"

run-go-client: 
	go build -o main .
	go run main.go

