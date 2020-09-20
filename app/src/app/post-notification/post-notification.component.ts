import { Component, OnInit, Input } from '@angular/core';
import { PostNotification } from '../services/data.service';

@Component({
  selector: 'app-message',
  templateUrl: './post-notification.component.html',
  styleUrls: ['./post-notification.component.scss'],
})
export class PostNotificationComponent implements OnInit {
  @Input() postNotification: PostNotification;

  constructor() { }

  ngOnInit() {}

  isIos() {
    const win = window as any;
    return win && win.Ionic && win.Ionic.mode === 'ios';
  }

  openReddit(link: string) {
    window.open(link);
  }
}
