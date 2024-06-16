import { createFeatureSelector } from '@ngrx/store'

import * as routerSelectors from '../../../navigation/state';

import { SearchState } from '../reducers';

export const SearchFeatureName = 'search';

export interface AppState extends routerSelectors.AppState {
    search: SearchState;
}

export const selectFeature = createFeatureSelector<AppState, SearchState>(SearchFeatureName);