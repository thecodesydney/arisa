from app.chatbot.routes import send_report

email = 'kevin_foong@yahoo.com'
report_name = 'test.txt'
send_report('kevin_foong@yahoo.com', 'test.txt')
print('User at {} has been emailed with attachment to report {}'.format(email, report_name))
