import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EffectsModule } from '@ngrx/effects';
import { StoreRouterConnectingModule } from '@ngrx/router-store';

import { RoutingEffects } from './state/effects';
import { LanRouterSerializer } from './state/serializer';

@NgModule({
    declarations: [],
    exports: [ ],
    imports: [
        CommonModule,
        EffectsModule.forFeature([RoutingEffects]),
        StoreRouterConnectingModule.forRoot({
            serializer: LanRouterSerializer
        }),
    ]
})
export class NavigationModule { }