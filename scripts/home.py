from flask import Flask, request, render_template
import json

app = Flask(__name__)
votes = []

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr

        # Check if the user has already voted
        for vote in votes:
            if vote['user_agent'] == user_agent and vote['ip_address'] == ip_address:
                return render_template('voted.html', user_agent=user_agent, ip_address=ip_address)

        # Log the vote
        votes.append({'user_agent': user_agent, 'ip_address': ip_address})
        with open('votes.json', 'w') as file:
            json.dump(votes, file)

        return render_template('thank_you.html', user_agent=user_agent, ip_address=ip_address)

    return render_template('vote.html')

if __name__ == '__main__':
    app.run()
