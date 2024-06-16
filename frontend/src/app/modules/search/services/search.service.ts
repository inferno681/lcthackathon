import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable} from 'rxjs';

import { AppUrlService } from './app-url.service';

import { ContentModel } from '../models';

@Injectable({
    providedIn: 'root'
})
export class SearchService {

    constructor(private http: HttpClient, private urls: AppUrlService) { }

    loadContent(query: string): Observable<any> {
        const url = this.urls.loadContent(query);
        return this.http.get<any>(url);
    }

}