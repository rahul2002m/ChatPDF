css = """
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 65px;
  max-height: 65px;
  object-fit: cover;
}
.chat-message.user .avatar img {
  max-width: 75px;
  max-height: 75px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712010.png"">
    </div>
    <div class="message">{{message}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.vhv.rs/dpng/d/10-101173_icon-tel-png-transparent-png.png">
    </div>
    <div class="message">{{message}}</div>
</div>
"""
