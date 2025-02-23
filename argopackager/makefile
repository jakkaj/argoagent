build_a:
	./build_image.sh date_wf_step

build_b:
	./build_image.sh wikipedia_wf_step

build_c:
	./build_image.sh summarise_wf_step

build: build_a build_b build_c



run:
	docker run -it --rm --env-file summarise_wf_step/.env k3d-registry.localhost:5000/summarise_wf_step
clean:
	docker rmi $(IMAGE_NAME)
