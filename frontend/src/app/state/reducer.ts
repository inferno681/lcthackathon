import { createReducer, on, Action, ActionReducer, MetaReducer } from '@ngrx/store';
import * as Actions from './actions';

export interface RootState {
    currentLang: string | null;
}

export const initialState: RootState = {
    currentLang: 'ru'
};

const rootReducers = createReducer(
    initialState
);

export function reducer(state: RootState | undefined, action: Action) {
    return rootReducers(state, action);
}
