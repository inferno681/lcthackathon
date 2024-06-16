import { createSelector } from '@ngrx/store';

import { AppState, selectFeature } from './states';
import { SearchState } from '../reducers';
import { ContentModel } from '../../models';

export const getContent = createSelector(
    selectFeature,
    (state: SearchState) => state.content
)