import { Component } from '@angular/core';
import { ChatService } from './chat.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  showChat = false;
  userQuestion = '';
  messages: { sender: string, text: string }[] = [];

  constructor(private chatService: ChatService) {}
  toggleChat() {
      if (this.showChat) {
    // User is closing the chat → clear messages
    this.messages = [];
    this.userQuestion = '';
      }

    this.showChat = !this.showChat;
  }
  

  sendMessage() {
    if (!this.userQuestion.trim()) return;

    this.messages.push({ sender: 'You', text: this.userQuestion });

    this.chatService.askQuestion(this.userQuestion).subscribe(response => {
      this.messages.push({ sender: 'Bot', text: response.answer });
      this.userQuestion = '';
    });
  }
}
