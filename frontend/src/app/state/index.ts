import { createFeatureSelector, createSelector } from '@ngrx/store';

import { RootState } from './reducer';

export const CoreFeatureName = 'router';

export interface AppState {
    router: RootState;
}

const selectFeature = createFeatureSelector<AppState, RootState>(CoreFeatureName);