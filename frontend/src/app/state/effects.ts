import { Injectable } from '@angular/core';
import { Actions, ofType, createEffect } from '@ngrx/effects';
import { of } from 'rxjs';
import { switchMap, catchError, map, withLatestFrom, mergeMap, mapTo, filter, tap } from 'rxjs/operators';
import { Store } from '@ngrx/store';

import { ModalService } from '../shared/services';
import { AddVideoComponent } from '../popups';
import { LayoutService} from '../services'

import * as actions from './actions';

@Injectable()
export class RootEffects {
    constructor(private actions$: Actions,
        private store$: Store,
        private modals: ModalService,
        private service: LayoutService
    ) { }

    showAddVideoPopups$ = createEffect(() => this.actions$.pipe(
        ofType(actions.showAddVideoPopups),
        tap(() => this.modals.show(AddVideoComponent, {
            width: '25%',
            minWidth: 670
        }))
        ), { dispatch: false }
    );

    addVideo$ = createEffect(()=> this.actions$.pipe(
        ofType(actions.addVideo),
        mergeMap((item)=> this.service.addVideo(item.addVideoModel))

    ));
}
