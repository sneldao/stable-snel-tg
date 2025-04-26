from telegram import Update
from telegram.ext import ContextTypes
from ..services.crypto_service import CryptoService
from typing import Optional

class AnalysisHandlers:
    def __init__(self):
        self.crypto_service = CryptoService()
        
    async def price_change_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ch command - Get price change analysis."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /ch bitcoin")
            return
            
        coin_id = context.args[0].lower()
        period = '7d'  # Default to 7 days
        
        if len(context.args) > 1:
            period = context.args[1].lower()
            
        data = await self.crypto_service.get_price_change(coin_id, period)
        
        if not data:
            await update.message.reply_text(f"Could not find price change data for {coin_id}")
            return
            
        message = (
            f"📊 {coin_id.upper()} Price Change Analysis ({data['period']}):\n\n"
            f"Current Price: ${data['current_price']:,.2f}\n"
            f"Price Change: {data['price_change']:+.2f}%\n"
            f"24h High: ${data['high_24h']:,.2f}\n"
            f"24h Low: ${data['low_24h']:,.2f}\n\n"
            f"All Time High: ${data['ath']:,.2f} ({data['ath_date']})\n"
            f"All Time Low: ${data['atl']:,.2f} ({data['atl_date']})"
        )
        await update.message.reply_text(message)
        
    async def roi_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /roi command - Get Return on Investment analysis."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /roi bitcoin")
            return
            
        coin_id = context.args[0].lower()
        data = await self.crypto_service.get_roi(coin_id)
        
        if not data:
            await update.message.reply_text(f"Could not find ROI data for {coin_id}")
            return
            
        message = (
            f"💰 {coin_id.upper()} ROI Analysis:\n\n"
            f"Current Price: ${data['current_price']:,.2f}\n\n"
            f"From All Time High (${data['ath']:,.2f} on {data['ath_date']}):\n"
            f"ROI: {data['ath_roi']:+.2f}%\n\n"
            f"From All Time Low (${data['atl']:,.2f} on {data['atl_date']}):\n"
            f"ROI: {data['atl_roi']:+.2f}%"
        )
        await update.message.reply_text(message)
        
    async def ath_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ath command - Get All Time High analysis."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /ath bitcoin")
            return
            
        coin_id = context.args[0].lower()
        data = await self.crypto_service.get_ath_analysis(coin_id)
        
        if not data:
            await update.message.reply_text(f"Could not find ATH data for {coin_id}")
            return
            
        message = (
            f"📈 {coin_id.upper()} All Time High Analysis:\n\n"
            f"Current Price: ${data['current_price']:,.2f}\n"
            f"All Time High: ${data['ath']:,.2f}\n"
            f"ATH Date: {data['ath_date']}\n"
            f"Current Price vs ATH: {data['ath_percentage']:.2f}%\n"
            f"Days Since ATH: {data['days_since_ath']}"
        )
        await update.message.reply_text(message) 