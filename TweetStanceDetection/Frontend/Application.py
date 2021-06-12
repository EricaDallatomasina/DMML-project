from Backend.Classification import *
from Backend.scraper import *
import warnings
warnings.filterwarnings("ignore")


# launch the application from terminal with: python -m  Frontend.Application
# in this way all the paths are relative to the root directory


def main():
    while True:
        print("Premi q per uscire, enter per classificare\n")
        if input() == 'q':
            print("Exit")
            break
        else:
            print("Inserisci parametri per la classificazione: (Lascia vuoto se vuoi i valori di default)\n")
            print("DA (default \"2021-03-01\" , formato \"YYYY-mm--gg\"):", end='  ')
            date_from = input()
            print("A (default data corrente, formato \"YYYY-mm--gg\"):", end='  ')
            date_to = input()
            print("Vaccino (default tutti):", end='  ')
            vaccine = input()
            print("")

            addTweets()
            classify(start_date=date_from, end_date=date_to, vaccine=vaccine)


if __name__ == "__main__":
    main()
