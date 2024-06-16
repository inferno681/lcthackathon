import { Injectable } from '@angular/core';

import { appHelpers } from '../../../shared/services';
import { environment } from '../../../app.config';

@Injectable({
    providedIn: 'root'
})
export class AppUrlService {

    constructor() { }

    loadContent(query: string): string{
        return this.getUrlWithParams({seach_str: query}, `search`)
    }

    private getUrlWithParams(parameters: { [key: string]: any }, ...parts: string[]): string {
        return `${environment.apiBaseUrl}${appHelpers.getUrlWithParams({ path: ['v1', ...parts], parameters })}`;
    }
}
