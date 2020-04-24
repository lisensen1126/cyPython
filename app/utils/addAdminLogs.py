from app import db
def addLogs(userLogs):
    db.session.add(userLogs)
    db.session.commit()