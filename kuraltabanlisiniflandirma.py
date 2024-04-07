import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv("persona.csv")

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df.head()
df.shape
df.info()

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

df.pivot_table(values="PRICE", index="COUNTRY", aggfunc="count")

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()

# Soru 7: SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby(['COUNTRY']).agg({"PRICE":"mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby(['SOURCE']).agg({"PRICE": "mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"mean"}).head()

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df.head()

#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
agg_df.reset_index(inplace=True)
agg_df.head()

#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'
# AGE değişkeninin nerelerden bölüneceğini belirtelim:


agg_df["AGE"].min()
agg_df["AGE"].max()

bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

# pd.crosstab(agg_df["AGE"],agg_df["AGE_CAT"])

# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# Dikkat!
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.


agg_df.columns

for row in agg_df.values:
    print(row)

agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_cat']].apply(lambda x: '_'.join(x).upper(),axis=1)

agg_df["customers_level_based"] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'AGE_CAT']].apply(lambda x: '_'.join(x).upper(),axis=1)
agg_df.head()

agg_df1 = agg_df[["customers_level_based", "PRICE"]]
agg_df1.head()

agg_df1["customers_level_based"].value_counts()

# Bu sebeple segmentlere göre groupby yaptıktan sonra price ortalamalarını almalı ve segmentleri tekilleştirmeliyiz.
agg_df1 = agg_df1.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df1.head()
# customers_level_based index'te yer almaktadır. Bunu değişkene çevirelim.
agg_df1.reset_index(inplace=True)
agg_df1.head()

# kontrol edelim. her bir persona'nın 1 tane olmasını bekleriz:
agg_df1["customers_level_based"].value_counts()


# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,
# segmentleri betimleyiniz,

agg_df1["SEGMENT"]= pd.qcut(agg_df1["PRICE"], 4, labels=["D", "C", "B", "A"]) #küçükten büyüğe !!!
agg_df1.head(30)


agg_df1.groupby("SEGMENT").agg({"PRICE": ["mean", "min", "max", "sum", "count"]})

#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df1[agg_df1["customers_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente girer ve ortalama ne kadar gelir kazandırması beklenir?
new_user2 = "FRA_IOS_FEMALE_31_40"
agg_df1[agg_df1["customers_level_based"] == new_user2]
