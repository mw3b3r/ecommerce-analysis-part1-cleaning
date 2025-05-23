# -*- coding: utf-8 -*-
"""Sales transactions cleaning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MknZtd1fYJekejSOZXwl2GwUXmLoVOEm
"""

# importy + import csv

import pandas as pd
import numpy as np

df = pd.read_csv('sales_transaction.csv')
df.info()

#  Počet řádků: 536 350 TransactionNo, ProductNo, ProductName, Date, Country jsou textové (object)
#  TransactionNo a ProductNo bychom převést na int, jsou čistě číselné.
#  CustomerNo má 536 295 hodnot z 536 350 – chybí nám 55 hodnot (pravděpodobně anonymní zákazníci).
#  Datum (Date) je stále object –  převést na datetime.
#  Price je float64 (OK), Quantity je int64 (OK).
#  Quantity je u některých položek v záporných hodnotách

df.head()

# Změna formátu času na evropský
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y").dt.strftime("%d/%m/%Y")

# Změna čísla zákazníka na celé číslo
df["CustomerNo"] = df["CustomerNo"].astype("Int64")

df["CustomerNo"].dtype  # Mělo by vrátit Int64
df["CustomerNo"].head(10)  # Pro kontrolu prvních 10 hodnot

# TransactionNo a ProductNo - převod z object na int
df["TransactionNo"] = pd.to_numeric(df["TransactionNo"], errors='coerce').astype('Int64') # Handle non-numeric values by converting to NaN, then to Int64
df["ProductNo"] = pd.to_numeric(df["ProductNo"], errors='coerce').astype('Int64') # Apply similar logic to ProductNo column

df["TransactionNo"].dtype  # Mělo by vrátit Int64
df["TransactionNo"].head(10)  # Pro kontrolu prvních 10 hodnot

df["ProductNo"].dtype  # Mělo by vrátit Int64
df["ProductNo"].head(10)  # Pro kontrolu prvních 10 hodnot

#  Kontrola formátu
df.info()

# kontrola nulových hodnot
df.isna().sum()

#  Co s nulovými hodnotami?
#  TransactionNo má 8 585 chybějících hodnot → chybějící číslo transakce
#  Quantity má 8585 záporných hodnot - vratky a reklamace?
#  ProductNo má 50 921 chybějících hodnot → chybějící produktové číslo
#  CustomerNo má 55 chybějících hodnot → chybějící ID zákazníka

# Seznam položek s chybějícím produktovým číslem
df_missing_product = df[df["ProductNo"].isna()]
df_missing_product.head()

# Opakuje se produkt s chybějícím číslem?
df[df["ProductName"] == "Small Marshmallows Pink Bowl"]

# Má produkt vůbec někde produktové číslo, které by se dalo přiřadit?
df[(df["ProductName"] == "Small Marshmallows Pink Bowl") & (df["ProductNo"].notna())]

# Bude potřeba produktům přiřadit jejich vlastní produktová čísla. JAká je aktuální obsazenost čísel?
# Najdeme minimum a maximum pouze mezi platnými produktovými čísly (bez NaN)
min_product_no = df["ProductNo"].min()
max_product_no = df["ProductNo"].max()

print(f"Nejmenší produktové číslo: {min_product_no}")
print(f"Největší produktové číslo: {max_product_no}")

# Vyfiltrování unikátních názvů produktů, kde chybí ProductNo
unique_missing_products = df[df["ProductNo"].isna()]["ProductName"].unique()

# Výpis výsledku
print(f"Počet unikátních produktů bez ProductNo: {len(unique_missing_products)}")
# print(unique_missing_products)

# Najdeme unikátní názvy produktů bez ProductNo
missing_product_numbers = df[df["ProductNo"].isna()]["ProductName"].unique()

# Vytvoříme číselnou řadu pro nové ProductNo, začínající od 1 000 001
new_numbers = {name: num for name, num in zip(missing_product_numbers, range(1000001, 1000001 + len(missing_product_numbers)))}

# Přiřadíme nové číslo všem produktům se stejným názvem
df.loc[df["ProductNo"].isna(), "ProductNo"] = df["ProductName"].map(new_numbers)

# Převod na celé číslo
df["ProductNo"] = df["ProductNo"].astype("Int64")

# Výsledek - ukázka prvních řádků
df[df["ProductNo"] >= 1000001].head()

# Produktové číslo - kontrola nulových hodnot
df_missing_product = df[df["ProductNo"].isna()]
df_missing_product.head()

# Shrnutí:
# Produktová čísla komplet doplněna. Vytvořena produktová ředa od 1 000 001, pro 912 neočíslovaných typů produktů.

# Kontrola nulových hodnot TransactionNo
df_missing_transaction = df[df["TransactionNo"].isna()]
df_missing_transaction.head()

# Počet záznamů se záporným množstvím Quantity
negative_quantity_count = df[df["Quantity"] < 0].shape[0]
print(f"Počet položek se záporným Quantity: {negative_quantity_count}")

# Náhled prvních 10 řádků se záporným Quantity
negative_quantity_rows = df[df["Quantity"] < 0].head(10)
print(negative_quantity_rows)

# Počet chybějících TransactionNO a záporných Quantity je stejný - 8585
# Vytvořím sloupec, který identifikuje vrácené objednávky, přidáním nového sloupce true/false

df["ReturnFlag"] = df["Quantity"] < 0
# df.head()
df["ReturnFlag"].value_counts()

df.head()

# Nulové hodnoty po úpravě:

#  TransactionNo má 8 585 chybějících hodnot → ponecháno beze změny, stejný počet jako Quantity-
#  Quantity má 8585 záporných hodnot - připojen sloupec ReturnFlag True/False
#  ProductNo má 50 921 chybějících hodnot → chybějící produktové číslo doplněno
#  CustomerNo má 55 chybějících hodnot → chybějící ID zákazníka

# kontrola nulových hodnot
df.isna().sum()

# Filtrujeme řádky, kde CustomerNo je NaN a zároveň ReturnFlag je True
missing_customers_with_returns = df[df["CustomerNo"].isna() & df["ReturnFlag"]]

# Počet těchto záznamů
count_missing_customers_with_returns = missing_customers_with_returns.shape[0]

print(f"Počet záznamů, kde chybí CustomerNo a zároveň je ReturnFlag=True: {count_missing_customers_with_returns}")

# 54 záznamů s chybějícím CustomerNo a ReturnFlag=True:
  # Může se jednat o anonymní vrácení zboží, například v kamenné prodejně bez potřeby evidovat zákazníka.
  # Mohlo by to být také špatně zanesené v systému.

# 1 záznam s chybějícím CustomerNo, ale ReturnFlag=False:
  # To je divné – znamená to, že někdo něco koupil, ale nevíme kdo.
  # Může to být chyba v datech, nebo šlo o interní transakci.

# Více než 8500 vrácených objednávek, kde je číslo zákazníka uvedeno:
  # Zákazník zboží vrátil a bylo to spojeno s jeho účtem.
  # To je v souladu s běžným procesem e-shopů, kde jsou vrácené objednávky spárovány se zákazníkem.

# 1 záznam s chybějícím CustomerNo, ale ReturnFlag=False:

missing_customer_no_return_false = df[df["CustomerNo"].isna() & (df["ReturnFlag"] == False)]
print(missing_customer_no_return_false)

# Existují další stejné TransactionNo 558245?

same_transaction = df[df["TransactionNo"] == "558245"]
print(same_transaction)

# Ponechám prázdný, nelze spojit s žádnou jinou stransakcí pod uvedeným TransactionNo

# 54 záznamů s chybějícím CustomerNo a ReturnFlag=True:
# Chci najít, zda stejný produkt a stejný počet kusů existoval v kladné hodnotě (tedy jako nákup) před datem vrácení.
# Vybereme jednu vrácenou položku (něco s ReturnFlag=True).
# Najdu nejbližší předchozí záznam, kde byl stejný produkt koupen ve stejném množství (ale s kladnou hodnotou Quantity).
# Pokud se podaří najít, podívám se, jestli odpovídá CustomerNo (pokud je uvedeno).



# Vybereme jeden produkt, který byl vrácen
test_product = df[df["Quantity"] < 0]["ProductNo"].iloc[0]

# Spočítáme celkový počet prodaných kusů (Quantity > 0)
total_sold = df[(df["ProductNo"] == test_product) & (df["Quantity"] > 0)]["Quantity"].sum()

# Spočítáme celkový počet vrácených kusů (Quantity < 0)
total_returned = abs(df[(df["ProductNo"] == test_product) & (df["Quantity"] < 0)]["Quantity"].sum())

print(f"Testujeme produkt číslo: {test_product}")
print(f"Celkový prodej: {total_sold}")
print(f"Celkové vrácení: {total_returned}")

# Najdeme záznamy, kde byl produkt prodán
sold_data = df[(df["ProductNo"] == test_product) & (df["Quantity"] > 0)]

# Najdeme záznamy, kde byl produkt vrácen
returned_data = df[(df["ProductNo"] == test_product) & (df["Quantity"] < 0)]

# Spojíme data podle zákazníka
merged_data = sold_data.merge(returned_data, on="CustomerNo", suffixes=("_sold", "_returned"))

# Zobrazíme prvních pár výsledků
print(merged_data[["CustomerNo", "TransactionNo_sold", "Quantity_sold", "TransactionNo_returned", "Quantity_returned"]].head(10))

# JAk to vypadá u ostatních produktů? Jedná se o anomálii, že chybí číslo transakce při návratu?

# Najdeme produkty, které byly kompletně vráceny
fully_returned_products = df.groupby("ProductNo")["Quantity"].sum()
fully_returned_products = fully_returned_products[fully_returned_products == 0]

# Zobrazíme prvních pár výsledků
print(f"Počet produktů, které byly kompletně vráceny: {len(fully_returned_products)}")
print(fully_returned_products.head(10))

# Filtrujeme jen tyto produkty
returned_products_df = df[df["ProductNo"].isin(fully_returned_products.index)]

# Zobrazíme prvních pár řádků
print(returned_products_df.head(10))

# Paper Craft Little Birdie (23843)
# Jasné spojení: Pouze jeden zákazník (16446), který produkt koupil a vrátil ve stejný den.

df.loc[(df["ProductNo"] == 23843) & (df["CustomerNo"].isna()), "CustomerNo"] = 16446

# Hanging Ridge Glass T-Light Holder (21655)
# Zákazník: 13672 – koupil 24 ks a vrátil 2x po 12 ks.

df.loc[(df["ProductNo"] == 21655) & (df["CustomerNo"].isna()), "CustomerNo"] = 13672

# Black Cherry Lights (1000858)
# Dva zákazníci:
# Zákazník 13672 koupil 8 ks, vrátil 4 ks.
# Zákazník 15823 koupil 4 ks, vrátil všechny.

df.loc[(df["ProductNo"] == 1000858) & (df["Quantity"] == -4), "CustomerNo"] = 13672
df.loc[(df["ProductNo"] == 1000858) & (df["Quantity"] == -4), "CustomerNo"] = 15823

# White Beaded Garland String 20light (85047)
# Prodány 3 ks různým zákazníkům, vráceny 3 ks.
# Zákazník 16222 koupil 1 ks.
# Zákazník 15311 a 13319 koupili 2 ks.
# 1 vrácený ks → CustomerNo = 16222
# 2 vrácené ks → CustomerNo = 13319

df.loc[(df["ProductNo"] == 85047) & (df["Quantity"] == -1), "CustomerNo"] = 16222
df.loc[(df["ProductNo"] == 85047) & (df["Quantity"] == -2), "CustomerNo"] = 13319

# Glass Cake Cover And Plate (21667)
# Pouze jeden zákazník (17841) koupil a vrátil stejný počet.

df.loc[(df["ProductNo"] == 21667) & (df["CustomerNo"].isna()), "CustomerNo"] = 17841

# Kde ještě chybí CustomerNo?

missing_customers = df[df["CustomerNo"].isna()]
print("Počet zbývajících záznamů bez CustomerNo:", len(missing_customers))
display(missing_customers)

# 1 záznam - chybí Quantity a CustomerNO, ale má TRansactionNo - ??

# Najdeme všechny záznamy se stejným TransactionNo jako "Plasters In Tin"
related_transactions = df[df["TransactionNo"] == 563662]

# Zobrazíme výsledek
display(related_transactions)

# Najdeme řádek, kde chybí CustomerNo u "Plasters In Tin"
df.loc[
    (df["TransactionNo"] == 563662) & (df["ProductNo"] == 22554),
    ["CustomerNo", "Price", "Quantity"]
] = [12729, 11.94, 12]

# Zkontrolujeme opravený řádek
display(df[df["TransactionNo"] == 563662])

# 📌 Shrnutí úprav dat:
# ✅ TransactionNo – Opraveno u chybějících záznamů na základě data a čísla zákazníka.
# ✅ ProductNo – Chybějící produktová čísla doplněna podle názvu produktu.
# ✅ Quantity – Přidán nový sloupec ReturnFlag, aby bylo jasné, že záporné hodnoty znamenají vrácení zboží.
# ✅ CustomerNo – 9 nevyplněných hodnot ponecháno prázdných, protože chybí možnost je dohledat.

df.to_csv("cleaned_sales_data.csv", index=False, encoding="utf-8")



