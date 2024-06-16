import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

import { Observable} from 'rxjs';

import { AppUrlService } from './app-url.service';

import { AddVideoModel } from '../models';

@Injectable({
    providedIn: 'root'
})
export class LayoutService {

    constructor(private http: HttpClient, private urls: AppUrlService) { }

    addVideo(addVideoModel: AddVideoModel): Observable<any>{
        const url = this.urls.addVideo();
        return this.http.post<any>(url, addVideoModel)
    }
}
