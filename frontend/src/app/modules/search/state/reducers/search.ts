import { on } from '@ngrx/store';

import * as actions from '../actions';
import { SearchState } from './states';

export const SEARCH_REDUCERS = [
    on(actions.loadContentSuccess, (state: SearchState, {content}) => ({...state, content: content})),
    on(actions.loadContentFails, (state: SearchState) => ({...state, content: []}))
]