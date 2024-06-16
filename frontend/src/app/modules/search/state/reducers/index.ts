import { createReducer, on, Action } from '@ngrx/store';

import * as actions from '../actions';
import { SearchState, initialState } from './states';
import { SEARCH_REDUCERS } from './search';

export * from './states';

const seachReducers = createReducer(
    initialState,
    on(actions.empty, (state: SearchState) => ({ ...state })),

    ...SEARCH_REDUCERS
);

export function reducer(state: SearchState | undefined, action: Action) {
    return seachReducers(state, action);
}