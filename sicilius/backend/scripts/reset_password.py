import sys
from os.path import abspath, dirname

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import user as crud_user

def reset_user_password():
    """
    Komut satırından alınan e-posta adresi için kullanıcı şifresini sıfırlar.
    """
    if len(sys.argv) != 3:
        print("Kullanım: python -m scripts.reset_password <email> <yeni_sifre>")
        sys.exit(1)

    email_to_update = sys.argv[1]
    new_password = sys.argv[2]

    db: Session = SessionLocal()
    try:
        user = crud_user.user.get_by_email(db, email=email_to_update)
        if not user:
            print(f"Hata: '{email_to_update}' e-posta adresine sahip kullanıcı bulunamadı.")
            return

        # crud_user.update fonksiyonu 'password' anahtarı ile düz metin şifre bekler
        # ve hash'leme işlemini kendi içinde yapar.
        user_update_data = {"password": new_password}
        crud_user.user.update(db, db_obj=user, obj_in=user_update_data)
        
        print(f"'{email_to_update}' e-posta adresli kullanıcının şifresi başarıyla güncellendi.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_user_password()
