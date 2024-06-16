import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { NgModule, isDevMode } from '@angular/core';
import { BrowserAnimationsModule, provideAnimations } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { META_REDUCERS, StoreModule } from '@ngrx/store';
import { SignalREffects, signalrReducer } from 'ngrx-signalr-core';
import { routerReducer, StoreRouterConnectingModule } from '@ngrx/router-store';
import { FileUploadModule } from 'ng2-file-upload';
import { MatDialogModule } from '@angular/material/dialog';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routes';
import { SharedModule } from './shared/shared.module';
import { RootEffects } from './state/effects';

import { reducer } from './state/reducer';

import { LAYOUTS } from './layout';
import { POPUPS } from './popups';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { EffectsModule } from '@ngrx/effects';

@NgModule({
  declarations: [
    AppComponent,
    ...LAYOUTS,
    ...POPUPS
  ],
  imports: [
    CommonModule,
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FileUploadModule,
    AppRoutingModule,
    RouterModule,
    StoreModule.forRoot({
      router: routerReducer,
      core: reducer,
    }, {}),
    StoreDevtoolsModule.instrument({ maxAge: 25, logOnly: !isDevMode() }),
    EffectsModule.forRoot([RootEffects, SignalREffects]),
    SharedModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }