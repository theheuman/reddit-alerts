import { Injectable } from '@angular/core';

export interface PostNotification {
  subreddit: string;
  text: string;
  whatFilterMatched: string;
  postLink: string;
  id: number;
  read: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private postNotifications: PostNotification[] = [
    {
      subreddit: 'buildapcsales',
      text: '[SSD] WB SN750 Black 1tb $130 ($140-20)',
      whatFilterMatched: 'ssd',
      postLink: 'https://www.reddit.com/r/buildapcsales/comments/iwkvim/game_cyberpunk_2077_4994_perorder/',
      id: 0,
      read: false
    },
    {
      subreddit: 'buildapcsales',
      text: '[GPU] PowerColor AMD 5700xt $400 ($450-50)',
      whatFilterMatched: '5700xt',
      postLink: 'https://www.reddit.com/r/buildapcsales/comments/iwkvim/game_cyberpunk_2077_4994_perorder/',
      id:  1,
      read: false
    }
  ];

  constructor() { }

  public getPostNotifications(): PostNotification[] {
    return this.postNotifications;
  }

  public getPostNotificationsById(id: number): PostNotification {
    this.postNotifications[id].read = true;
    return this.postNotifications[id];
  }

  public addPostNotifications(newPostNotification: PostNotification) {
    this.postNotifications.push(newPostNotification);
  }
}
