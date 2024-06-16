import { Component, OnInit  } from '@angular/core';
import { Store } from '@ngrx/store';

import * as actions from '../../state/actions';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.sass'
})

export class LayoutComponent implements OnInit {

  constructor(private store$: Store) { }

  ngOnInit(): void { }

  showAddVideoPopups(){
    this.store$.dispatch(actions.showAddVideoPopups());
  }
}
