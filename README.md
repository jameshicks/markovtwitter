markovtwitter
=============

A markov chain twitter client

Inputs: a corpus text file, one sentence per line.

Generate a database for random text generation with 
```./make_db.py --corpus text.corpus --out database.db --order 2```. 
Increasing the order of the chain will make more realistic text at the expense of recovering the original text from the training corpus.

Generate random text (once the database is created), with:
```./generate_text.py --db database.db ```

Examples
=============

This algorithm was initially trained on ~30,000 journal article titles from [Pubmed](http://www.ncbi.nlm.nih.gov/pubmed/), a database of biomedical research abstracts. Some generated examples:
* Craving in patients with frontotemporal lobar degeneration and poor prognostic indicators: results from the University of California at Davis, USA (1984-2004).
* Fatigue, health-related quality of Life in storage at room Temperature.
* Acupuncture treatment for periorbital melanosis in children with vesicoureteral reflux.
* The Physiologic Effects of BMI, Smoking and Risk of cholecystectomy: a prospective Descriptive Study Using Validated Instruments.
* Extended mathematical model of amyotrophic lateral sclerosis.
* miR-137 impairs the elimination of shelterin components in the cytoplasmic domain Regulates Cell death in pneumococcal meningitis.
* Should infected laparotomy wounds be treated with hot acid etching Procedures on participant safety and efficacy of computed tomography analysis of the offspring.
