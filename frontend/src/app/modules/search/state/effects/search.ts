import { Injectable } from '@angular/core';
import { Actions, ofType, createEffect } from '@ngrx/effects';
import { of } from 'rxjs';
import { switchMap, catchError, map, withLatestFrom, mergeMap, mapTo, filter, tap } from 'rxjs/operators';
import { Store } from '@ngrx/store';

import { SearchService} from '../../services'

import * as actions from '../actions';

@Injectable()
export class SearchEffects {
    constructor(private actions$: Actions,
        private service: SearchService
    ) { }

    loadContent$ = createEffect(() => this.actions$.pipe(
        ofType(actions.loadContent),
        mergeMap((item) => this.service.loadContent(item.query).pipe(
            map(content => actions.loadContentSuccess({content})),
            catchError(error => of(actions.loadContentFails({error})))
        ))
    ));
}