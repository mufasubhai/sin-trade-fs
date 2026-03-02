import os
import resend
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from src.config import BackendConfig


class EmailService:
    @staticmethod
    def is_within_allowed_hours() -> bool:
        try:
            pacific_tz = ZoneInfo("America/Los_Angeles")
            now_pacific = datetime.now(pacific_tz)
            hour = now_pacific.hour
            return 8 <= hour < 22
        except Exception as e:
            logging.warning(f"Error checking time: {e}, defaulting to send")
            return True

    @staticmethod
    def send_trade_signal_alert(user_email: str, user_id: int, signals: list) -> bool:
        if not signals:
            logging.warning(f"No signals provided for user {user_id}")
            return True
            
        if not EmailService.is_within_allowed_hours():
            logging.info(f"Outside allowed hours (8am-10pm PT), skipping email to {user_email}")
            EmailService._store_email_notification(
                user_id=user_id,
                email=user_email,
                subject="Skipped - Outside Hours",
                body="Email skipped due to outside allowed hours",
                signals=signals,
                status="skipped"
            )
            return True

        if not BackendConfig.RESEND_API_KEY:
            logging.error("RESEND_API_KEY not configured")
            return False

        if not BackendConfig.RESEND_EMAIL_FROM:
            logging.error("RESEND_EMAIL_FROM not configured")
            return False

        try:
            signal_summary = EmailService._build_signal_summary(signals)
            
            if not signals or len(signals) == 0:
                logging.warning(f"No valid signals for user {user_id}")
                return True
                
            subject = f"SinTrade Alert: {signal_summary['action']} - {signal_summary['total']} Signal(s)"
            html_body = EmailService._build_html_email_body(signals, signal_summary)
            
            try:
                logging.info(f"Sending email to {user_email} with {len(signals)} signals")
                logging.info(f"Subject: {subject}")
                logging.info(f"From: {BackendConfig.RESEND_EMAIL_FROM}")
                
                params = {
                    "from": BackendConfig.RESEND_EMAIL_FROM,
                    "to": "aapodaca@gmail.com",
                    # "to": user_email,
                    "subject": subject,
                    "html": html_body,
                }
                
                response = resend.Emails.send(params)
                
                logging.info(f"Email response: {response}")
                
                if response is None:
                    raise Exception("Resend returned None response")
                
                logging.info(f"Email sent to {user_email}: {response}")
                
                EmailService._store_email_notification(
                    user_id=user_id,
                    email=user_email,
                    subject=subject,
                    body=html_body,
                    signals=signals,
                    status="sent"
                )
            except Exception as e:
                import traceback
                logging.error(f"Error sending email: {e}")
                logging.error(f"Traceback: {traceback.format_exc()}")
                EmailService._store_email_notification(
                    user_id=user_id,
                    email=user_email,
                    subject="Failed - Error",
                    body=str(e) + "\n" + traceback.format_exc(),
                    signals=signals,
                    status="failed"
                )
            
            return True
            
        except Exception as e:
            logging.error(f"Error sending trade signal alert: {e}")
            return False
            
    @staticmethod
    def _build_signal_summary(signals: list) -> dict:
        if not signals:
            return {"buy_count": 0, "sell_count": 0, "action": "Hold", "total": 0}
            
        buy_count = sum(1 for s in signals if s and s.get("signal_type") == "buy")
        sell_count = sum(1 for s in signals if s and s.get("signal_type") == "sell")
        
        action = "Buy & Sell" if buy_count > 0 and sell_count > 0 else "Buy" if buy_count > 0 else "Sell" if sell_count > 0 else "Hold"
        
        return {
            "buy_count": buy_count,
            "sell_count": sell_count,
            "action": action,
            "total": len(signals)
        }

    @staticmethod
    def _build_html_email_body(signals: list, summary: dict) -> str:
        if not signals:
            return "<p>No signals available.</p>"
            
        signal_rows = ""
        for i, signal in enumerate(signals, 1):
            if not signal:
                continue
            signal_type = (signal.get("signal_type") or "unknown").upper()
            confidence = signal.get("confidence_score", 0) or signal.get("confidence", 0) or 0
            price = signal.get("price_at_signal", 0) or 0
            ticker_code = signal.get("ticker_code") or "UNKNOWN"
            is_crypto = signal.get("is_crypto", False) or False
            
            color = "#22c55e" if signal_type == "BUY" else "#ef4444" if signal_type == "SELL" else "#6b7280"
            asset_type = "Crypto" if is_crypto else "Stock"
            
            signal_rows += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">
                    <strong style="color: {color};">{signal_type}</strong>
                </td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{ticker_code}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{asset_type}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">${price:.2f}</td>
                <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{confidence*100:.1f}%</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f9fafb; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="background-color: #1f2937; padding: 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px;">SinTrade Trading Alert</h1>
                </div>
                
                <div style="padding: 24px;">
                    <p style="margin-top: 0; color: #374151; font-size: 16px;">
                        <strong>Action Required:</strong> {summary['action']}
                    </p>
                    
                    <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                        <div style="flex: 1; background-color: #f3f4f6; padding: 16px; border-radius: 6px; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #22c55e;">{summary['buy_count']}</div>
                            <div style="font-size: 14px; color: #6b7280;">Buy</div>
                        </div>
                        <div style="flex: 1; background-color: #f3f4f6; padding: 16px; border-radius: 6px; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #ef4444;">{summary['sell_count']}</div>
                            <div style="font-size: 14px; color: #6b7280;">Sell</div>
                        </div>
                    </div>
                    
                    <h3 style="color: #374151; font-size: 16px; margin-bottom: 12px;">Signal Details</h3>
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
                        <thead>
                            <tr style="background-color: #f3f4f6;">
                                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb;">Type</th>
                                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb;">Ticker</th>
                                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb;">Asset</th>
                                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb;">Price</th>
                                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb;">Confidence</th>
                            </tr>
                        </thead>
                        <tbody>
                            {signal_rows}
                        </tbody>
                    </table>
                    
                    <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">
                        <em>These signals are generated using sine-wave analysis. The recommended hold time is approximately 4 hours.</em>
                    </p>
                    
                    <p style="color: #6b7280; font-size: 14px;">
                        Log in to your <a href="http://localhost:5173" style="color: #3b82f6;">SinTrade dashboard</a> for more details.
                    </p>
                </div>
                
                <div style="background-color: #f9fafb; padding: 16px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                        Sent by SinTrade • Trading alerts based on sine-wave analysis
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    @staticmethod
    def _store_email_notification(
        user_id: int,
        email: str,
        subject: str,
        body: str,
        signals: list,
        status: str = "pending"
    ) -> None:
        try:
            if not BackendConfig.supabase:
                logging.warning("No Supabase connection, cannot store email notification")
                return
            
            BackendConfig.supabase.table("ml_email_notifications").insert({
                "user_id": user_id,
                "email": email,
                "subject": subject,
                "body": body,
                "status": status,
                "signals": signals,
                "created_at": datetime.now().isoformat(),
            }).execute()
            
            logging.info(f"Stored email notification for user {user_id} with status {status}")
            
        except Exception as e:
            logging.error(f"Error storing email notification: {e}")
