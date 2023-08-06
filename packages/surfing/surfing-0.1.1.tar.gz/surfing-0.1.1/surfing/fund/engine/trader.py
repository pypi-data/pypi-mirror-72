from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import AssetTrade, FundTrade, FundPosition, FundWeight
from ...data.struct import AssetTradeParam, FundTradeParam
from ...data.struct import AssetTradeCache, FundWeightItem
from . import Helper
from .asset_helper import FAHelper
import numpy as np
import math

class AssetTrader(Helper):

    def __init__(self, asset_param: AssetTradeParam=None):
        self.asset_param = asset_param or AssetTradeParam()

    def calc_asset_trade(self, dt,
                               cur_position: AssetPosition,
                               cur_price: AssetPrice,
                               target_allocation: AssetWeight):
        cur_mv = AssetValue(prices=cur_price, positions=cur_position)
        tot_mv = cur_mv.sum()

        trades = []
        launch_trade = False
        for index_id, target_weight in target_allocation.__dict__.items():
            if index_id != 'cash':
                target_amt = tot_mv * target_weight
                p = cur_price.__dict__[index_id]
                cur_amt = cur_mv.__dict__[index_id]
                if abs(target_amt - cur_amt) > tot_mv * self.asset_param.MinCountAmtDiff:
                    amount = abs(target_amt - cur_amt)
                    is_buy = target_amt > cur_amt
                    if is_buy:
                        trades.append(AssetTrade(
                            index_id=index_id,
                            mark_price=p,
                            amount=amount,
                            is_buy=is_buy,
                            submit_date=dt
                        ))
                    else:
                        trades.append(AssetTrade(
                            index_id=index_id,
                            mark_price=p,
                            volume=amount/p,
                            is_buy=is_buy,
                            submit_date=dt
                        ))
                launch_trade = launch_trade or abs(target_amt - cur_amt) > tot_mv * self.asset_param.MinActionAmtDiff

        if not launch_trade:
            return cur_position, None
        else:
            trades.sort(key=lambda x: x.is_buy)
            new_position = cur_position.copy()
            for trd in trades:
                new_position.update(trd)
            return new_position, trades

    def finalize_trade(self, dt, trades: list,
                            t1_price: AssetPrice,
                            bt_position: AssetPosition):
        pendings = []
        traded_list = []
        if trades is None or len(trades) == 0:
            return pendings, traded_list
        # TODO: if some trades needs more time
        for trd in trades:
            # TODO: commision calculate
            #trd.commission = ?
            # update position
            trd.trade_price = t1_price.__dict__[trd.index_id]
            trd.volume = trd.volume if trd.volume else (trd.amount / trd.trade_price)
            trd.trade_date = dt
            if not trd.is_buy:
                if not(bt_position.__dict__[trd.index_id] - trd.volume > -1e-8):
                    print(f'trade volume exceeds, adjusted to pos (index_id){trd.index_id} (vol){trd.volume} (is_buy){trd.is_buy} (pos){bt_position.__dict__[trd.index_id]}')
                    trd.volume = bt_position.__dict__[trd.index_id]
            trd.amount = trd.volume * trd.trade_price    
            if self.asset_param.EnableCommission:
                if trd.is_buy:
                    trd.volume = trd.amount / trd.trade_price / (1 + self.asset_param.PurchaseDiscount * self.asset_param.AssetPurchaseRate[trd.index_id])
                    trd.commission = trd.volume * trd.trade_price * self.asset_param.PurchaseDiscount * self.asset_param.AssetPurchaseRate[trd.index_id]
                else:
                    trd.commission = trd.amount * self.asset_param.RedeemDiscount * self.asset_param.AssetRedeemRate[trd.index_id]
                    trd.amount -= trd.commission
            else:
                trd.commission = 0
            bt_position.update(trd)
            traded_list.append(trd)
        return pendings, traded_list

class FundTrader(AssetTrader):

    def __init__(self, asset_param: AssetTradeParam=None, fund_param: FundTradeParam=None):
        AssetTrader.__init__(self, asset_param=asset_param)
        self.fund_param = fund_param or FundTradeParam()

    def set_helper(self, fa_helper: FAHelper):
        self.fa_helper = fa_helper

    def has_expired_fund(self, cur_fund_position:FundPosition, _prep_fund_score:dict):
         # 如果持仓基金 没有分数， 返回True
        pos_fund_set = {fund_id for fund_id, fund_pos_i in cur_fund_position.funds.items() if fund_pos_i.volume > 0}
        score_set = set()
        for index_id, pos_i in _prep_fund_score.items():
            score_set.update(pos_i.keys())
        return bool(pos_fund_set.difference(score_set))

    # to be deprecated
    def calc_fund_trade(self, dt, fund_weight: FundWeight, cur_fund_position: FundPosition,
                            cur_fund_nav: dict,
                            fund_purchase_fees: dict,
                            fund_redeem_fees: dict) -> list:
        new_fund_position = cur_fund_position.copy()
        fund_trades = []
        # return trade list
        fund_tot_mv, cur_fund_wgts = cur_fund_position.calc_mv_n_w(fund_navs=cur_fund_nav)
        all_funds = {}
        # prepare fund candidates and its index_id
        for fund_id, fund_wgt_item in fund_weight.funds.items():
            all_funds[fund_id] = fund_wgt_item.index_id
        for fund_id, fund_pos_item in cur_fund_position.funds.items():
            all_funds[fund_id] = fund_pos_item.index_id
        # calc trade
        for fund_id, index_id in all_funds.items():
            target_fund_amt = fund_weight.get_wgt(fund_id) * fund_tot_mv
            cur_fund_volume = cur_fund_position.get_volume(fund_id) or 0
            p = cur_fund_nav[fund_id]
            cur_fund_amt = cur_fund_volume * p

            if abs(target_fund_amt - cur_fund_amt) > fund_tot_mv * self.fund_param.MinCountAmtDiff or (target_fund_amt == 0 and cur_fund_amt > 0):
                # TODO: commision and 如果是清某一只基金的逻辑，清空可以执行
                is_buy = target_fund_amt > cur_fund_amt
                if is_buy:
                    _trade = FundTrade(
                        fund_id=fund_id,
                        index_id=index_id,
                        mark_price=p,
                        amount=abs(target_fund_amt - cur_fund_amt),
                        is_buy=is_buy,
                        submit_date=dt
                    )
                else:
                    _trade = FundTrade(
                        fund_id=fund_id,
                        index_id=index_id,
                        mark_price=p,
                        volume=abs(target_fund_amt - cur_fund_amt)/p,
                        is_buy=is_buy,
                        submit_date=dt
                    )
                fund_trades.append(_trade)
                #print(f'(fund){fund_id} (p){p} (amt0){cur_fund_amt} (amt1){target_fund_amt} (idx){index_id} (amt){abs(target_fund_amt - cur_fund_amt)} (direc) {target_fund_amt > cur_fund_amt} ')

        fund_trades.sort(key=lambda x: x.is_buy)
        for _trade in fund_trades:
            new_fund_position.update(_trade)
        return new_fund_position, fund_trades

    def finalize_trade(self, dt, trades: list,
                            t1_price: AssetPrice,
                            bt_position: AssetPosition,
                            cur_fund_position: FundPosition,
                            cur_fund_nav: dict,
                            cur_fund_unit_nav: dict,
                            fund_purchase_fees: dict,
                            fund_redeem_fees: dict,
                            disproved_set: set):

        if trades is None or len(trades) == 0:
            return [], []

        pendings = []
        traded_list = []
        # TODO: if some trades needs more time
        for trd in trades:
            if trd.fund_id not in disproved_set:
                trd.is_permitted_fund = True
            else:
                trd.is_permitted_fund = False
            trd.trade_price = cur_fund_nav[trd.fund_id]
            trd.fund_unit_nav = cur_fund_unit_nav[trd.fund_id]
            trd.volume = trd.volume if trd.volume else (trd.amount / trd.trade_price)
            trd.amount = trd.amount if trd.amount else (trd.volume * trd.trade_price)
            trd.fund_unit_volume = trd.amount / trd.fund_unit_nav
            trd.trade_date = dt
            if not trd.is_buy:
                cur_vol = cur_fund_position.get_volume(trd.fund_id)
                if not((cur_vol or 0) - trd.volume > -1e-8):
                    print(f'trade volume exceeds, adjusted to pos (fund_id){trd.fund_id} (vol){trd.volume} (is_buy){trd.is_buy} (pos){cur_vol}')
                    assert cur_vol is not None, 'sell fund with no current position!'
                    trd.volume = cur_vol
                    trd.amount = trd.volume * trd.trade_price
            if self.fund_param.EnableCommission:
                if trd.is_buy:
                    purchase_fee = fund_purchase_fees[trd.fund_id] * self.fund_param.PurchaseDiscount 
                    if np.isnan(purchase_fee):
                        #print(f'fund_id {trd.fund_id} purchase fee data not avaiable')
                        purchase_fee = 0
                    trd.volume = trd.amount / trd.trade_price / (1 + purchase_fee)
                    trd.commission = trd.volume * trd.trade_price * purchase_fee
                else:
                    redeem_fee = fund_redeem_fees[trd.fund_id] * self.fund_param.RedeemDiscount
                    if np.isnan(redeem_fee):
                        #print(f'fund_id {trd.fund_id} redeem fee data not avaiable')
                        redeem_fee = 0
                    trd.commission = trd.amount * redeem_fee
                    trd.amount -= trd.commission
            else:
                trd.commission = 0
            if trd.is_permitted_fund == False:
                print(f'trade is not permitted : {trd}')

            trade_status = cur_fund_position.update(trd)
            if trade_status:
                traded_list.append(trd)
            else:
                print(f'trade failed alert : {trd}')
        # get cur asset weight from fund weight
        cur_mv, cur_fund_weight = cur_fund_position.calc_mv_n_w(cur_fund_nav)
        fund_index_dic = {}
        for fund_id, fund_pos_item in cur_fund_position.funds.items():
            fund_index_dic[fund_id] = fund_pos_item.index_id
        asset_wgt = { _ : 0 for _ in set(fund_index_dic.values())}
        for fund_id, wgt_i in cur_fund_weight.items():
            index_id = fund_index_dic[fund_id]
            asset_wgt[index_id] += wgt_i
        # set index position:
        for index_id in asset_wgt:
            asset_p = t1_price.__dict__[index_id]
            amount = cur_mv * asset_wgt[index_id]
            bt_position.__dict__[index_id] = amount / asset_p
        # fund cash -> asset cash
        bt_position.cash = cur_fund_position.cash
        return pendings, traded_list

    def calc_trade(self, dt,
            tar_fund_weight: FundWeight,
            tar_asset_weight: AssetWeight,
            cur_fund_position: FundPosition,
            cur_asset_position: AssetPosition,
            cur_fund_nav: dict,
            cur_fund_score: dict,
            cur_asset_price: AssetPrice,
            fund_purchase_fees: dict,
            fund_redeem_fees: dict) -> list:
        '''
        v_asset_position, asset_trade_list = self.calc_asset_trade(dt, cur_asset_position, cur_asset_price, tar_asset_weight)
        if not asset_trade_list:
            return v_asset_position, asset_trade_list
        else:
            return self.calc_fund_trade(dt, tar_fund_weight, cur_fund_position, cur_fund_nav, fund_purchase_fees, fund_redeem_fees)
        '''
        index_max_diff = 0
        fund_max_diff = 0
        _index_max_diff_name = ''
        _fund_max_diff_name = ''

        cur_asset_mv = AssetValue(prices=cur_asset_price, positions=cur_asset_position)
        cur_asset_weight = cur_asset_mv.get_weight()

        fund_tot_mv, cur_fund_wgts = cur_fund_position.calc_mv_n_w(fund_navs=cur_fund_nav)

        index_fund_cache = []
        for index_id, index_tar_wgt in tar_asset_weight.__dict__.items():

            if index_id == 'cash':
                continue

            c = AssetTradeCache(index_id=index_id)
            c.index_tar_wgt = index_tar_wgt
            c.index_cur_wgt = cur_asset_weight.__dict__[index_id]
            c.index_diff = c.index_tar_wgt - c.index_cur_wgt
            if abs(c.index_diff) > index_max_diff:
                # TODO: 这里不需要加绝对值吗
                index_max_diff = abs(c.index_diff)
                _index_max_diff_name = index_id

            # calc funds in each index
            c.fund_cur_wgts = cur_fund_position.calc_mv_n_w(cur_fund_nav, index_id)[1]
            c.cur_fund_ids = set(c.fund_cur_wgts.keys())
            c.fund_scores = sorted(cur_fund_score.get(index_id, {}).items(), key=lambda item: item[1], reverse=True)
            c.fund_ranks = {info[0]: rank + 1 for rank, info in enumerate(c.fund_scores)}

            # allowed change logic
            c.proper_fund_num = self.fa_helper.get_max_fund_num(index_id)
            # print(index_id, len(c.fund_scores), c.proper_fund_num)
            allowed_max_ranking = min(len(c.fund_scores) * 0.3, 2 * c.proper_fund_num)

            # to start or others, cur_fund_ids is few
            if len(c.cur_fund_ids) < c.proper_fund_num:
                for fund_id, _score in c.fund_scores:
                    if fund_id not in c.cur_fund_ids:
                        c.cur_fund_ids.add(fund_id)
                        if len(c.cur_fund_ids) == c.proper_fund_num:
                            break
            assert len(c.cur_fund_ids) >= c.proper_fund_num, 'cur fund id candidate should be no less than proper_fund_num'

            # calc cur fund diff sum
            index_fund_sum_diff = 0
            for fund_id in c.cur_fund_ids:
                _rank = c.fund_ranks.get(fund_id)
                old_wgt = c.fund_cur_wgts.get(fund_id, 0)
                new_wgt = 1.0 / c.proper_fund_num if _rank and _rank <= allowed_max_ranking else 0
                fund_diff = new_wgt - old_wgt
                # print(f'calc fund_diff (fund_id){fund_id} (index_id){index_id} (fund_diff){fund_diff} (new_wgt){new_wgt} (old_wgt){old_wgt}')
                # TODO: 小于0时是否应该加上绝对值然后计入
                index_fund_sum_diff += abs(fund_diff)

            # TODO: index_tar_wgt和注释不一样
            if index_fund_sum_diff > fund_max_diff and index_tar_wgt > self.fund_param.DiffJudgeAssetWgtRequirement:
                fund_max_diff = index_fund_sum_diff
                _fund_max_diff_name = index_id

            index_fund_cache.append(c)

        # self.fund_param.DiffJudgeLambda = 0
        final_diff = self.fund_param.DiffJudgeLambda * fund_max_diff + (1 - self.fund_param.DiffJudgeLambda) * index_max_diff
        to_trade = final_diff > self.fund_param.DiffJudgeTolarance
        if to_trade:
            print(f' --- calc {dt} (to_trade){to_trade} (diff){final_diff} (lambda){self.fund_param.DiffJudgeLambda} (fund){fund_max_diff}/{_fund_max_diff_name} (index){index_max_diff}/{_index_max_diff_name}')

        new_fund_position = cur_fund_position.copy()
        fund_trades = []

        if to_trade:

            for c in index_fund_cache:
                funds = {}
                fund_selected_num = 0
                fund_selected_wgt = 0
                proper_fund_wgt = 1.0 / c.proper_fund_num if c.proper_fund_num > 0 else 0
                good_fund_to_sell = []
                to_cancel = set([])
                # 如果 cur_fund_ids 超过 proper_fund_num
                if len(c.cur_fund_ids) > c.proper_fund_num:
                    _d = {fund_id: c.fund_ranks.get(fund_id) for fund_id in c.cur_fund_ids}
                    _dd = sorted(_d.items(), key=lambda x: x[1], reverse=True)
                    for fund_id, _rank in _dd[:len(c.cur_fund_ids) - c.proper_fund_num]:
                        to_cancel.add(fund_id)
                        print(f'to_cancel (fund_id){fund_id} (rank){_rank}')

                for fund_id in c.cur_fund_ids:
                    _rank = c.fund_ranks.get(fund_id)
                    if _rank is None:
                        print(f'got a None rank when trying to trade, (index_id){c.index_id} (fund_id){fund_id} (dt){dt} (fund_scores){c.fund_scores} (fund_ranks){c.fund_ranks}')
                        to_cancel.add(fund_id)
                    _cur_wgt = c.fund_cur_wgts.get(fund_id, 0)
                    _tar_wgt = 0
                    if fund_id in to_cancel:
                        _tar_wgt = 0
                    elif _rank <= c.proper_fund_num:
                        # 当前持仓仍排名在前 proper_num 的基金，我们统一安排 1 / proper_num 的比例
                        _tar_wgt = proper_fund_wgt
                        if _cur_wgt * c.index_cur_wgt > _tar_wgt * c.index_tar_wgt:
                            good_fund_to_sell.append((fund_id, _rank, _cur_wgt * c.index_cur_wgt - _tar_wgt * c.index_tar_wgt))
                    elif _rank <= allowed_max_ranking:
                        # 如果排名在 proper_num + 1 ~ 2 * proper_num 的基金，
                        # 如果不足 1 / proper_num 的比例，则不变，如果多于 1 / proper_num，就减至 1 / proper_num。（只减少，不增加）
                        _tar_wgt = min(proper_fund_wgt, _cur_wgt * c.index_cur_wgt / c.index_tar_wgt)
                    else:
                        _tar_wgt = 0

                    fund_selected_wgt += _tar_wgt
                    fund_selected_num += 1 if _tar_wgt > 0 else 0

                    _wgt = FundWeightItem(fund_id=fund_id, index_id=c.index_id, asset_wgt=c.index_tar_wgt, fund_wgt_in_asset=_tar_wgt)
                    funds[fund_id] = _wgt

                assert fund_selected_wgt <= 1, f'[fund trade] tot fund wgt <= 1: {fund_selected_wgt}'

                # 如果当前比例还有剩余（步骤2中产生的）
                if fund_selected_wgt < 1 - 1e-5 and c.index_tar_wgt > 0:
                    tot_wgt_left = (1 - fund_selected_wgt) * c.index_tar_wgt
                    # 如果步骤1中前 proper_num 有哪个减少过，就按照排名高低revert这个减少
                    if len(good_fund_to_sell) > 0:
                        good_to_sell_list = sorted(good_fund_to_sell, key=lambda x: x[1])

                        for fund_id, _rank, _sell_wgt in good_to_sell_list:
                            print(f'one in good_to_sell_list, (index_id){c.index_id} (fund_id){fund_id} (rank){_rank} (sell_wgt){_sell_wgt}')
                            revert_wgt = min(tot_wgt_left, _sell_wgt)
                            funds[fund_id].add_tot_wgt(revert_wgt)
                            tot_wgt_left -= revert_wgt
                            if tot_wgt_left < 1e-5:
                                break

                    # 如果将减少的都处理完还有剩余，那么进入到特殊状态（SPECIAL）
                    if tot_wgt_left > 1e-5:
                        print(f"happy in SPECIAL CASE (proper num){c.proper_fund_num}")
                        assert fund_selected_num <= c.proper_fund_num, f'fund selected num {fund_selected_num} should le than proper fund num {c.proper_fund_num}!!'
                        # 对于SPECIAL，我们先看fund_selected_num是否已达到proper_num
                        if fund_selected_num < c.proper_fund_num:
                            # 如果否，从fund_score中按评分从高到低将不在当前持仓的基金每个都增加进去，最多不超过 1 / proper_num，直到fund_selected_num等于proper_num或剩余的量消耗光
                            for fund_id, _score in c.fund_scores:
                                if fund_id not in funds:
                                    _tar_wgt = min(proper_fund_wgt, tot_wgt_left / c.index_tar_wgt)
                                    _wgt = FundWeightItem(fund_id=fund_id, index_id=c.index_id, asset_wgt=c.index_tar_wgt, fund_wgt_in_asset=_tar_wgt)
                                    print(f'[SPECIAL] (index_id){c.index_id} (fund){fund_id} (score){_score} (rank){c.fund_ranks[fund_id]} (tar_wgt){_tar_wgt}')
                                    funds[fund_id] = _wgt
                                    fund_selected_num += 1
                                    tot_wgt_left -= _tar_wgt * c.index_tar_wgt
                                    if tot_wgt_left < 1e-5 or fund_selected_num == c.proper_fund_num:
                                        break

                        # 如果是，或fund_selected_num等于proper_num时剩余的量仍未消耗光
                        # 我们将剩余的比例平均分配给当前持仓的基金，以此来将剩余的量消耗光（分配后有可能超过 1 / proper_num，但实际在上边第4条中也有可能导致超过 1 / proper_num）
                        if tot_wgt_left > 1e-5:
                            funds_without_no_wgt = {fund_id: fund for fund_id, fund in funds.items() if fund.fund_wgt_in_asset > 0}
                            avg_wgt_left = tot_wgt_left / len(funds_without_no_wgt)
                            for fund_id, _wgt in funds_without_no_wgt.items():
                                print(f'[SPECIAL] (index_id){c.index_id} (fund){fund_id} (rank){c.fund_ranks[fund_id] if fund_id in c.fund_ranks else None} (avg_wgt_left){avg_wgt_left}')
                                _wgt.add_tot_wgt(avg_wgt_left)
                                tot_wgt_left -= avg_wgt_left
                                assert tot_wgt_left >= 0 or math.isclose(tot_wgt_left, 0, abs_tol=1e-05), f'tot_wgt_left less than zero!! {tot_wgt_left} (index_id){c.index_id}'

                    assert tot_wgt_left < 1e-5, f'special even failed: {c.index_id}'

                for fund_id, _wgt in funds.items():
                    target_fund_amt = _wgt.fund_wgt * fund_tot_mv
                    cur_fund_amt = c.fund_cur_wgts.get(fund_id, 0) * c.index_cur_wgt * fund_tot_mv
                    if abs(target_fund_amt - cur_fund_amt) > fund_tot_mv * self.fund_param.MinCountAmtDiff or (target_fund_amt == 0 and cur_fund_amt > 0):
                        p = cur_fund_nav[fund_id]
                        _trade = FundTrade(
                            fund_id=fund_id,
                            index_id=c.index_id,
                            mark_price=p,
                            amount=abs(target_fund_amt - cur_fund_amt),
                            is_buy=target_fund_amt > cur_fund_amt,
                            submit_date=dt,
                            is_to_cleanup=(target_fund_amt == 0 and cur_fund_amt > 0)
                        )
                        fund_trades.append(_trade)
                        print(f'(fund){fund_id} (index){c.index_id} (p){p} (rank){c.fund_ranks[fund_id] if fund_id in c.fund_ranks else 0} (cur_amt){cur_fund_amt} (tar_amt){target_fund_amt} (idx){c.index_id} (amt){abs(target_fund_amt - cur_fund_amt)}')

        fund_trades.sort(key=lambda x: x.is_buy)
        for _trade in fund_trades:
            new_fund_position.update(_trade)
        return new_fund_position, fund_trades
