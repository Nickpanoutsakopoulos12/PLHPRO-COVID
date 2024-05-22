import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():                                        #Kύρια δομή Προγράμματος
    plt.style.use('seaborn-v0_8')

    url = "https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/cases.csv"
    df = pd.read_csv(url)

    compare_dates(df)                             #Συνάρτηση Καρτέλας Δεδομένων
    pie_1(df)
    pie_2(df)
    vaccinations_and_actives(df)                 #Συνάρτηση συνολικών εμβολιασμών και ενεργών κρουσμάτων
    cases_deaths(df)                             #Συνάρτηση Επιβεβαιομένων Κρουσμάτων και Θανάτων
    hospitalized(df)




def compare_dates(df):

    df.set_index('id',inplace=True)                                                                         #To id θα γίνει το νέο index
    print("Καρτέλα Ημερήσιας Επισκόπησης: (Προηγούμενη Μέρα-Τωρινή Μέρα-Ποσοστιαία Διαφορά)")
    copied_df = df.copy(deep=True)                                                                          #Δημιουργία Αντιγράφου και μετονομασία στήλεων
    copied_df.rename(columns={'date':'Ημερομηνία','new_cases':'Νέα Κρούσματα','confirmed':'Επιβεβαιομένα Κρούσματα','new_deaths':'Νέες Απώλειες','total_deaths':'Συνολικές Απώλειες',
                       'new_tests':'Νέα Τέστ','positive_tests':"Θετικά Τέστ",'new_selftest':'Νέα Σελφτέστ','new_ag_tests':'Νέα Τέστ Αντισωμάτων',
                       'ag_tests':'Τέστ Αντισωμάτων','total_tests':'Συνολικά Τέστ','new_critical':'Νέοι Νοσηλευόμενοι Σε Κρίσιμη','total_vaccinated_crit':'Εμβολιασμένοι Σε Κρίσιμη',
                       'total_unvaccinated_crit':'Μη Εμβολιασμένοι Σε Κρίσιμη','total_critical':'Συνολικός Αριθμός Νοσηλευόμενων Σε Κρίσιμη','hospitalized':'Σε Νοσηλεία','icu_percent':'Ποσοστό σε ΜΕΘ',
                       'icu_out':'Εκτώς της ΜΕΘ','new_active':'Νέα Ενεργά Κρούσματα','active':'Ενεργά Κρούσματα','recovered':'Που Εχει Αναρρώσει','total_vaccinations':'Συνολικοί Εμβολιασμοί','reinfections':'Επαναμολύνσεις'},inplace=True)
    copied_df = copied_df.drop(columns=['total_selftest','total_foreign','total_unknown','beds_percent','discharged','total_domestic','total_reinfections'])       #Αφαίρεση κάποιων δεδομένων



    col_start = copied_df.columns.get_loc('Νέα Κρούσματα')                  #Επιλέγω ποιες στήλες θα εμφανιστούν
    col_end = copied_df.columns.get_loc('Επαναμολύνσεις')
    df3 = copied_df.iloc[[-2,-1],col_start:col_end]                          # Επιλέγω 2 τελευταίες γραμμές (2 τελευταίες μέρες)
    pct = df3.pct_change()                                                   #Υπολογίζω ποσοστιαία διαφορά των δύο μερών
    pct2 = pct.drop(pct.index[[0]])

    pct3 = pd.concat([df3,pct2])                                             #Ενώνω τις 2 καρτέλες,θα προβληθούν σε μορφή αναστρόφου πίνακα
    pct3.index = ['Προηγούμενη','Τωρινή','Διαφορά']
    print(pct3.transpose())

def cases_deaths(df):
    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1)                         #Δημιουργώ καρτέλα με 2 subplots
    ax1.plot(df.date,df.confirmed,label="Επιβεβαιωμένα Κρούσματα")
    ax2.plot(df.date,df.total_deaths,label="Συνολικές Απώλειες")

    ax1.legend()
    ax1.set_title("Επιβεβαιωμένα Κρούσματα")
    ax1.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax1.set_ylabel("Κρούσματα")
    plt.sca(ax1)
    plt.xticks(df.date[::182])                                              #Ο άξωνας χ (ημερομηνίες) θα είναι ανα εξάμηνα

    ax2.legend()
    ax2.set_title("Συνολικές Απώλειες")
    ax2.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax2.set_ylabel("Απώλειες")
    plt.ticklabel_format(axis="y", style='plain')                           #Αφαίρεση scientific notation
    plt.sca(ax2)
    plt.xticks(df.date[::182])

    plt.tight_layout()
    plt.show()

def vaccinations_and_actives(df):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

    ax1.plot(df.date, df.total_vaccinations, label="Αριθμός εμβολιασμών")

    ax2.plot(df.date, df.active)

    ax1.set_title("Συνολικοί εμβολιασμοί")
    ax1.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax1.set_ylabel("Εμβολιασμοί")
    plt.sca(ax1)
    plt.ticklabel_format(axis="y", style='plain')
    plt.xticks(df.date[::182])

    ax2.set_title("Συνολική Εξέλιξη Ενεργών Κρουσμάτων")
    ax2.set_xlabel('Ημερομηνίες (Ανα εξάμηνα)')
    ax2.set_ylabel("Αριθμός Ενεργών Κρουσμάτων")
    plt.sca(ax2)
    plt.xticks(df.date[::182])

    plt.tight_layout()
    plt.show()

def pie_1(df):
    tot_reinf =  df.iloc[-1,29]              #Eπαναμολύνσεις
    tot_vacc = df.iloc[-1,27]                # εμβολιασμοί
    tot_unkn = df.iloc[-1,26]                # αγνωστα κρούσματα

    naming = 'Συνολικές Επαναμολύνσεις','Συνολικοί Εμβολιασμοί','Συνολικά Αγνωστα Κρούσματα'
    plt.pie([tot_reinf,tot_vacc,tot_unkn],labels=naming,autopct='%1.1f%%')
    plt.title("Ποσοστά Συνολικών Επαναμολύνσεων,Εμβολιασμών και Άγνωστων Κρουσμάτων")
    plt.show()

def pie_2(df):
    tot_dom =  df.iloc[-1,25]
    tot_forgn = df.iloc[-1,24]

    naming = 'Συνολικά Εγχώρια Κρούσματα','Συνολικά Ξένα Κρούσματα'
    plt.pie([tot_dom,tot_forgn],labels=naming,autopct='%1.1f%%')
    plt.title("Ποσοστά Συνολικών Εγχωρίων και Ξένων Κρουσμάτων")
    plt.show()

def hospitalized(df):
    hospital = df.loc[df['hospitalized']>0]
    hospital_date = hospital.iloc[:,0]
    hospitalized = hospital.iloc[:,16]

    plt.bar(hospital_date,hospitalized,label="Νοσηλευόμενοι",width=1)

    plt.title("Κάρτα Νοσηλευόμενων")
    plt.xlabel("Ημερομηνίες")
    plt.ylabel("Αριθμός Νοσηλευόμενων")
    plt.xticks(hospital_date[::100])
    plt.show()



if __name__ == "__main__":
    main()
    print("Τέλος Προγράμματος!")
