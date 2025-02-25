build_a:
	./build_image.sh date_wf_step

build_b:
	./build_image.sh wikipedia_wf_step

build_c:
	./build_image.sh summarise_wf_step

build_d:
	./build_image.sh extra_key_statistics_wf

build: build_a build_b build_c build_d



run_summarise:
	docker run -it --rm --env-file summarise_wf_step/.env k3d-registry.localhost:5000/summarise_wf_step

run_wikipedia:
	docker run -it --rm k3d-registry.localhost:5000/wikipedia_wf_step

run_date:
	docker run -it --rm  k3d-registry.localhost:5000/date_wf_step


clean:
	docker rmi $(IMAGE_NAME)
