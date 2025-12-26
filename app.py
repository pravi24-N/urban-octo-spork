import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
app = Flask(__name__)
# Security: Allow frontend to talk to backend
CORS(app)

# Database Configuration (Update 'root' and 'password' with your MySQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('C:\Users\PRAVIGYA\OneDrive\Desktop\mortgage pwa\frontend')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security: SQLAlchemy ORM prevents SQL Injection automatically
db = SQLAlchemy(app)

# --- MODELS (Database Schema) ---
class UserAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(255), nullable=False)
    target_rate = db.Column(db.Float, nullable=False)

# New model: EMI Reminder
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    due_at = db.Column(db.DateTime, nullable=False)
    notified = db.Column(db.Boolean, default=False, nullable=False)

# --- ROUTES ---

@app.route('/api/rates', methods=['GET'])
def get_current_rates():
    # In a real app, this fetches from FRED/Government API.
    # For the project demo, we simulate a live rate to show fluctuation.
    simulated_rate = round(random.uniform(6.1, 7.2), 2)
    
    # Trend Logic (Simulated)
    trend = "down" if simulated_rate < 6.8 else "up"
    
    return jsonify({
        "current_rate": simulated_rate,
        "rate": simulated_rate,
        "trend": trend,
        "message": "Live rates fetched securely"
    })

@app.route('/api/calculate', methods=['POST'])
def calculate_true_cost():
    data = request.json
    
    # SECURITY: Input Validation
    # Prevent negative numbers or malicious payloads
    if not data or data.get('loanAmount', 0) < 0 or data.get('rate', 0) < 0:
        return jsonify({"error": "Invalid input detected"}), 400

    principal = float(data.get('loanAmount'))
    rate = float(data.get('rate'))
    years = int(data.get('tenure'))
    cibil_score = int(data.get('cibilScore', 750))  # Default CIBIL score if not provided
    
    # 1. CIBIL Score Based Rate Adjustment
    rate_adjustment = 0
    if cibil_score < 600:
        rate_adjustment = 2.0  # Poor credit
    elif cibil_score < 650:
        rate_adjustment = 1.5  # Fair credit
    elif cibil_score < 750:
        rate_adjustment = 0.5  # Good credit
    else:
        rate_adjustment = 0.0  # Excellent credit
    
    adjusted_rate = rate + rate_adjustment
    
    # 2. Standard EMI Math with adjusted rate
    monthly_rate = adjusted_rate / 100 / 12
    months = years * 12
    emi = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    
    # 3. The "True Cost" Logic (Hidden Fees)
    # Estimates: Tax ~1.2% yearly, Insurance ~0.5%, Maint ~1%
    monthly_tax = (principal * 0.012) / 12
    monthly_insurance = (principal * 0.005) / 12
    monthly_maintenance = (principal * 0.01) / 12  # The USP Feature
    
    total_monthly_hidden = monthly_tax + monthly_insurance + monthly_maintenance
    total_hidden_costs = total_monthly_hidden * months
    
    # 4. Calculate totals
    total_interest = (emi * months) - principal
    total_amount_payable = principal + total_interest + total_hidden_costs
    
    return jsonify({
        "base_emi": round(emi, 2),
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_amount": round(total_amount_payable, 2),
        "true_monthly_cost": round(emi + total_monthly_hidden, 2),
        "hidden_costs": round(total_hidden_costs, 2),
        "interest_rate_adjustment": round(rate_adjustment, 2),
        "breakdown": {
            "principal_interest": round(emi, 2),
            "taxes_maintenance": round(total_monthly_hidden, 2)
        }
    })
@app.route('/api/set-alert', methods=['POST'])
def set_alert():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided", "status": "error"}), 400
        
        user_id = data.get('uuid')
        target = data.get('target')
        
        if not user_id or target is None:
            return jsonify({"error": "Missing uuid or target", "status": "error"}), 400
        
        # Validate target is a valid number
        try:
            target_float = float(target)
        except (ValueError, TypeError):
            return jsonify({"error": "Target must be a valid number", "status": "error"}), 400
        
        # Simulate current rate and determine immediate notification
        current_rate = round(random.uniform(6.1, 7.2), 2)
        notified = False
        if current_rate <= target_float:
            notified = True

        # Save to MySQL securely via ORM
        new_alert = UserAlert(user_uuid=user_id, target_rate=target_float)
        db.session.add(new_alert)
        db.session.commit()
        
        return jsonify({
            "message": "Alert set anonymously!", 
            "status": "success", 
            "notified": notified, 
            "current_rate": current_rate
        }), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"Error in set_alert: {str(e)}")
        return jsonify({
            "error": f"Database error: {str(e)}", 
            "status": "error"
        }), 500

@app.route('/api/alert', methods=['POST'])
def alert_alias():
    # backward-compatible alias for frontend
    return set_alert()

# --- REMINDERS ENDPOINTS ---
from datetime import datetime, timezone

@app.route('/api/reminders', methods=['POST'])
def create_reminder():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided", "status": "error"}), 400
        user_id = data.get('uuid')
        title = data.get('title') or 'EMI Reminder'
        amount = data.get('amount')
        due_at_raw = data.get('due_at')
        if not user_id or not due_at_raw:
            return jsonify({"error": "Missing uuid or due_at", "status": "error"}), 400
        try:
            raw = due_at_raw
            # Accept ISO with 'Z' (UTC) by replacing it with +00:00 for fromisoformat
            if isinstance(raw, str) and raw.endswith('Z'):
                raw = raw.replace('Z', '+00:00')
            due_at = datetime.fromisoformat(raw)
            # If timezone-aware, convert to UTC and store naive UTC datetime
            if due_at.tzinfo is not None:
                due_at = due_at.astimezone(timezone.utc).replace(tzinfo=None)
        except Exception:
            return jsonify({"error": "Invalid due_at format. Use ISO format (e.g., 2025-12-17T19:00:00Z or with timezone offset)", "status": "error"}), 400
        reminder = Reminder(user_uuid=user_id, title=title, amount=amount, due_at=due_at)
        db.session.add(reminder)
        db.session.commit()
        return jsonify({"message": "Reminder created", "status": "success", "reminder": {"id": reminder.id}}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error in create_reminder: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}", "status": "error"}), 500

@app.route('/api/reminders', methods=['GET'])
def list_reminders():
    try:
        reminders = Reminder.query.order_by(Reminder.due_at.asc()).all()
        data = [{
            "id": r.id,
            "user_uuid": r.user_uuid,
            "title": r.title,
            "amount": r.amount,
            "due_at": r.due_at.isoformat() + 'Z',
            "notified": r.notified
        } for r in reminders]
        return jsonify({"reminders": data, "count": len(data)}), 200
    except Exception as e:
        print(f"Error in list_reminders: {e}")
        return jsonify({"error": "Could not fetch reminders", "details": str(e)}), 500

@app.route('/api/reminders/due', methods=['GET'])
def due_reminders():
    try:
        now = datetime.utcnow()
        due = Reminder.query.filter(Reminder.due_at <= now, Reminder.notified == False).all()
        data = [{
            "id": r.id,
            "user_uuid": r.user_uuid,
            "title": r.title,
            "amount": r.amount,
            "due_at": r.due_at.isoformat() + 'Z'
        } for r in due]
        return jsonify({"reminders": data, "count": len(data)}), 200
    except Exception as e:
        print(f"Error in due_reminders: {e}")
        return jsonify({"error": "Could not fetch due reminders", "details": str(e)}), 500

@app.route('/api/reminders/<int:reminder_id>/notify', methods=['POST'])
def mark_reminder_notified(reminder_id):
    try:
        r = Reminder.query.get(reminder_id)
        if not r:
            return jsonify({"error": "Reminder not found"}), 404
        r.notified = True
        db.session.commit()
        return jsonify({"message": "Reminder marked notified"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error in mark_reminder_notified: {e}")
        return jsonify({"error": "Could not update reminder", "details": str(e)}), 500


@app.route('/api/alerts', methods=['GET'])
def list_alerts():
    """Return recent saved alerts so frontend/dev can confirm persistence."""
    try:
        alerts = UserAlert.query.order_by(UserAlert.id.desc()).limit(50).all()
        data = [{
            "id": a.id,
            "user_uuid": a.user_uuid,
            "target_rate": a.target_rate
        } for a in alerts]
        return jsonify({"alerts": data, "count": len(data)}), 200
    except Exception as e:
        print(f"Error in list_alerts: {e}")
        return jsonify({"error": "Could not fetch alerts", "details": str(e)}), 500


@app.route('/api/gov-news', methods=['GET'])
def gov_news():
    # NOTE: In production this should scrape or call official APIs.
    # For demo, return curated list of government news with dates.
    news = [
        {"title": "RBI Issues Guidelines on Housing Finance", "date": "Nov 28, 2025"},
        {"title": "Government launches Affordable Housing Scheme Update", "date": "Nov 15, 2025"},
        {"title": "Home Loan Eligibility Criteria Simplified", "date": "Oct 30, 2025"},
        {"title": "New Tax Benefits on Home Loan Interest Announced", "date": "Oct 10, 2025"}
    ]
    return jsonify({"news": news})

# --- AGENTS (Exposure) ENDPOINT ---
@app.route('/api/agents', methods=['GET'])
def agents():
    # Static list for demo; can be replaced with DB seeding/migration as needed
    agents = [
        {"name": "Anil Kapoor", "phone": "+91-98765-43210", "company": "Sunrise Lending"},
        {"name": "Priya Sharma", "phone": "+91-91234-56789", "company": "HomeFirst Advisors"},
        {"name": "Ramesh Iyer", "phone": "+91-99887-76655", "company": "Capital Housing"},
    ]
    return jsonify({"agents": agents, "count": len(agents)}), 200

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    # Use ASCII-only log to avoid Windows console encoding errors
    print("Database tables created successfully")

@app.route('/api/health', methods=['GET'])
def health():
    try:
        # Test database connection
        result = db.session.execute(db.text('SELECT 1')).fetchone()
        return jsonify({
            "status": "ok",
            "database": "connected",
            "message": "API is running"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Bind to all interfaces so the backend is reachable from other devices on the LAN
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
