.PHONY: install test analyse dashboard api

install:
	python -m pip install -r requirements.txt
	python -m pip install -e .

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

analyse:
	python run_analysis.py

dashboard:
	streamlit run dashboard.py

api:
	uvicorn ccs_platform.api:app --reload

