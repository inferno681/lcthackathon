import { Params } from '@angular/router';
import { RouterReducerState } from '@ngrx/router-store';
import { createFeatureSelector, createSelector } from '@ngrx/store';

export const RouterFeatureName = 'router';

export interface RouterStateUrl {
    url: string;
    params: Params;
    queryParams: Params;
    data?: { [key: string]: any };
}

export interface AppState {
    router: RouterReducerState<RouterStateUrl>;
}

export const selectRouterFeature = createFeatureSelector<
    AppState,
    RouterReducerState<RouterStateUrl>
>(RouterFeatureName);