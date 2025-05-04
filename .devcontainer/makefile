.PHONY: build update rebuild clean

build:
	python3 .devcontainer/build.py
update:
	python3 .devcontainer/build.py --update
rebuild:
	rm -rf /workspaces/work
	python3 .devcontainer/build.py
clean:
	rm -rf release