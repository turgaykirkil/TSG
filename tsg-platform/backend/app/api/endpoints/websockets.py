import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from supabase import create_client, ClientOptions
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/ws/stats")
async def websocket_stats_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket bağlantısı kabul edildi.")

    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY

    if not supabase_url or not supabase_key:
        logger.error("Supabase URL/KEY ayarlanmamış.")
        await websocket.close(code=1011, reason="Sunucu yapılandırma hatası.")
        return

    supabase = None
    listener_task = None
    try:
        # Supabase istemcisini Realtime seçeneği ile başlat
        supabase = await create_client(
            str(supabase_url),
            supabase_key,
            options=ClientOptions(
                auto_refresh_token=True,
                persist_session=True,
                realtime=True
            )
        )
        logger.info("Supabase client başarıyla oluşturuldu.")

        # Başlangıç verisini gönder
        try:
            logger.info("Başlangıç istatistikleri alınıyor...")
            response = await supabase.table("live_stats").select("*").limit(1).execute()
            if response.data:
                # Supabase'den gelen veri bir liste içinde tek bir obje olarak gelir
                initial_stats = {"type": "initial", "data": response.data[0]}
                await websocket.send_json(initial_stats)
                logger.info(f"Başlangıç istatistikleri gönderildi: {initial_stats}")
            else:
                logger.warning("'live_stats' tablosunda başlangıç verisi bulunamadı.")
        except Exception as e:
            logger.error(f"Başlangıç istatistikleri alınırken hata: {e}", exc_info=True)

        # Realtime değişikliklerini dinleyecek olan coroutine
        async def realtime_listener():
            def on_message(payload):
                try:
                    logger.info(f"Realtime mesajı alındı: {payload}")
                    # Gelen veriyi ana thread'deki WebSocket'e güvenli bir şekilde gönder
                    asyncio.run_coroutine_threadsafe(websocket.send_json(payload), asyncio.get_running_loop())
                except Exception as e:
                    logger.error(f"on_message içinde hata: {e}", exc_info=True)

            channel = supabase.realtime.channel("live_stats_changes")
            channel.on(
                "postgres_changes",
                {"event": "*", "schema": "public", "table": "live_stats"},
                on_message
            )
            await channel.subscribe()
            logger.info("Supabase Realtime kanalına abone olundu.")

            # Bağlantı kopana kadar bekle
            while websocket.client_state.name == 'CONNECTED':
                await asyncio.sleep(1)

        listener_task = asyncio.create_task(realtime_listener())
        await listener_task

    except WebSocketDisconnect:
        logger.info("WebSocket bağlantısı istemci tarafından kapatıldı.")
    except Exception as e:
        logger.error(f"WebSocket ana döngüsünde beklenmeyen hata: {e}", exc_info=True)
    finally:
        if listener_task and not listener_task.done():
            listener_task.cancel()
        if supabase:
            await supabase.realtime.close()
        logger.info("WebSocket bağlantısı ve kaynaklar temizlendi.")
