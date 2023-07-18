
#CREATED BY
# Ozan Toyran, 18/07/2023
from flask import Flask, request, jsonify

#Create an API Server

app = Flask(__name__)

@app.route("/rezervasyon", methods=["POST"])
def rezervasyon():
    data = request.get_json()

    vagonlar = data["Tren"]["Vagonlar"]

    RezervasyonYapilacakKisiSayisi = data["RezervasyonYapilacakKisiSayisi"]
    KisilerFarkliVagonlaraYerlestirilebilir = data["KisilerFarkliVagonlaraYerlestirilebilir"]
    
    RezervasyonYapilabilir=True
    YerlesimAyrinti=[ ]
 # Rezervasyona uygunluğu kontrol et
    if RezervasyonYapilacakKisiSayisi>0:
        for vagon in vagonlar:
            vagon_adi= vagon["Ad"]
            kapasite = vagon["Kapasite"]
            dolu_koltuklar = vagon["DoluKoltukAdet"]


            doluluk = dolu_koltuklar/kapasite *100.
            bos_koltuk= kapasite*0.7-dolu_koltuklar #gerçek kapasitemiz online rezervasyonlar için %70

            if doluluk > 70.:   #Vagon doluluğu %70'in üzerindeyse vagonu es geç
                continue

            if RezervasyonYapilabilir:

#==================Yolcuları tercihlerine uygun yerleştir========================

                if KisilerFarkliVagonlaraYerlestirilebilir:
                    if bos_koltuk >= RezervasyonYapilacakKisiSayisi:

                        kisi_sayisi=RezervasyonYapilacakKisiSayisi

                        YerlesimAyrinti.append({"VagonAdi": vagon_adi,"KisiSayisi":round(kisi_sayisi)})      
                        #Bu kısım çıktıda ters sırayla basılıyor. nedenini çözemedim henüz.               
                    


                    else:
                        kisi_sayisi=bos_koltuk

                        RezervasyonYapilacakKisiSayisi=RezervasyonYapilacakKisiSayisi-bos_koltuk   

                        YerlesimAyrinti.append({
                            "VagonAdi": vagon_adi, 
                            "KisiSayisi":round(kisi_sayisi)
                           
                        }) 
#===============Yolcular farklı vagonda olmak istemiyorsa========================
                else:     
                    if bos_koltuk >= RezervasyonYapilacakKisiSayisi:

                        kisi_sayisi=RezervasyonYapilacakKisiSayisi

                        YerlesimAyrinti.append({
                            "KisiSayisi":round(kisi_sayisi),
                            "VagonAdi": vagon_adi                            
                        })
                        continue 


            
    response = {
        "RezervasyonYapilabilir": True,
        "YerlesimAyrinti": YerlesimAyrinti
    }

    return jsonify(response), 202

if __name__== "__main__":
  app.run(debug=True)
