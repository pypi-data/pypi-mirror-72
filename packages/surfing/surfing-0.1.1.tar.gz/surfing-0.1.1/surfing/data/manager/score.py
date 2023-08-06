
from typing import Dict, Any, Set
from collections import defaultdict
from ..struct import FundScoreParam, ScoreFilter, ScorePenaltyParams
from .data_tables import FundDataTables
import dataclasses
import pandas as pd
import re
import math
import numpy as np


@dataclasses.dataclass
class IndicatorLoc:
    alpha: int = 0
    fee_rate: int = 1
    track_err: int = 2
    beta: int = 3


@dataclasses.dataclass
class ScoreFunc:

    alpha: float = 0  # weight of alpha
    beta: float = 0  # weight of abs(1-beta), or beta's deviation from 1
    track_err: float = 0  # weight of track_err
    fee_rate: float = 0  # weight of fee_rate

    def get(self, data):
        return self.alpha * data[IndicatorLoc.alpha] + self.beta * abs(1-data[IndicatorLoc.beta]) + self.track_err * data[IndicatorLoc.track_err] + self.fee_rate * data[IndicatorLoc.fee_rate]


class FundScoreManager:

    def __init__(self, score_filter=ScoreFilter(), score_penalty_param=ScorePenaltyParams()):
        self.params = None
        self.dts = None
        # 归一化之后的评分
        # self.funcs = {
        #     'hs300': ScoreFunc(alpha=0.3, beta=-0.6, fee_rate=-0.1),
        #     'csi500': ScoreFunc(alpha=0.8, beta=-0.2),
        #     'gem': ScoreFunc(alpha=0.05, beta=-0.50, track_err=-0.45),
        #     'national_debt': ScoreFunc(alpha=0.32, beta=-0.33, track_err=-0.35),
        #     'mmf': ScoreFunc(alpha=0.6, fee_rate=-0.3, track_err=-0.1),
        #     'sp500rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),
        #     'gold': ScoreFunc(alpha=0.15, fee_rate=0, track_err=-0.85),
        # }
        '''
        # weekly indicator mean of std on each day each index
        {'alpha_std': {'csi500': 0.081316,
                        'gem': 0.060555,
                        'gold': 0.014478,
                        'hs300': 0.050694,
                        'mmf': 0.0063286,
                        'national_debt': 0.0751936,
                        'sp500rmb': 0.0163182},
        'fee_rate_std': {'csi500': 0.0031425,
                            'gem': 0.0043791,
                            'gold': 0.0031,
                            'hs300': 0.002674,
                            'mmf': 0.00083814,
                            'national_debt': 0.002321,
                            'sp500rmb': 0.0022616},
        'track_err_std': {'csi500': 0.0568387,
                        'gem': 0.0554576,
                        'gold': 0.024641,
                        'hs300': 0.04155,
                        'mmf': 0.000555,
                        'national_debt': 0.052457,
                        'sp500rmb': 0.0140498}}
        
        # 日因子均值
        {'gold': {'alpha_mean': -0.00145, 'fee_mean': 0.00793, 'track_mean': 0.06711},
        'sp500rmb': {'alpha_mean': -0.0038, 'fee_mean': 0.01029,'track_mean': 0.02805},
        'mmf': {'alpha_mean': 0.00998, 'fee_mean': 0.00325, 'track_mean': 0.0021},
        'csi500': {'alpha_mean': 0.02104, 'fee_mean': 0.00806, 'track_mean': 0.07783},
        'hs300': {'alpha_mean': 0.02763, 'fee_mean': 0.00889, 'track_mean': 0.04522},
        'national_debt': {'alpha_mean': 0.03921, 'fee_mean': 0.00573, 'track_mean': 0.02394},
        'gem': {'alpha_mean': -0.02174, 'fee_mean': 0.00868, 'track_mean': 0.05726}}

        # 日因子 std
        'csi500': {'alpha_std': 0.08291, 'fee_rate': 0.0031, 'track_err': 0.06534},
        'hs300': {'alpha_std': 0.0444, 'fee_rate': 0.00266, 'track_err': 0.03939},
        'sp500rmb': {'alpha_std': 0.01625, 'fee_rate': 0.00228, 'track_err': 0.01088},
        'mmf': {'alpha_std': 0.00917, 'fee_rate': 0.00084, 'track_err': 0.00123},
        'national_debt': {'alpha_std': 0.08303,'fee_rate': 0.00229,'track_err': 0.05373},
        'gem': {'alpha_std': 0.04332, 'fee_rate': 0.00464, 'track_err': 0.04749},
        'gold': {'alpha_std': 0.03312, 'fee_rate': 0.00311, 'track_err': 0.04839}

        # 周因子std
        self.funcs_weekly = {
            'hs300': ScoreFunc(alpha=0.3/0.05069, beta=-0.6, fee_rate=-0.1/0.002674),
            'csi500': ScoreFunc(alpha=0.8/0.081316, beta=-0.2),
            'gem': ScoreFunc(alpha=0.05/0.060555, beta=-0.50, track_err=-0.45/0.0554576),
            'national_debt': ScoreFunc(alpha=0.3/0.07519359, beta=-0.25, track_err=-0.45/0.052457),
            'mmf':ScoreFunc(alpha=0.6/0.0063286, fee_rate=-0.3/0.0008381, track_err=-0.1/0.000555),
            'sp500rmb': ScoreFunc(fee_rate=-0.2/0.002261574, track_err=-0.8/0.014049778),
            'gold': ScoreFunc(alpha=0.15/0.01447791, fee_rate=-0/0.0031002, track_err=-0.85/0.02464),
        }
 
        '''
        self.funcs = {
            'hs300': ScoreFunc(alpha=0.3/ 0.0444, beta=-0.6, fee_rate=-0.1/ 0.00266),
            'csi500': ScoreFunc(alpha=0.8/ 0.08291, beta=-0.2),
            'gem': ScoreFunc(alpha=0.05/0.04332, beta=-0.50, track_err=-0.45/0.04749),
            'national_debt': ScoreFunc(alpha=0.3/0.08303, beta=-0.5, track_err=-0.4/0.05373),
            'mmf': ScoreFunc(alpha=0.6/0.00917, fee_rate=-0.3/0.00084, track_err=-0.1/0.00123),
            'sp500rmb': ScoreFunc(fee_rate=-0.2/0.00228, track_err=-0.8/0.01088),
            'gold': ScoreFunc(alpha=0.15/0.03312, fee_rate=0, track_err=-0.85/0.04839),
            'hsi': ScoreFunc(alpha=0.3, fee_rate=-0.3, track_err=-0.4),# set default score equation
        }
        self.score_cache = defaultdict(dict)
        self.score_raw_cache = defaultdict(dict)
        self.score_filter = score_filter
        self.score_penalty_param = score_penalty_param
        self._size_and_com_hold_cache: Dict[Any, pd.Index] = {}

    def set_param(self, score_param: FundScoreParam):
        self.params = score_param

    def set_dts(self, dts: FundDataTables):
        self.dts = dts
        self.fund_id_to_name = self.dts.fund_info[['fund_id', 'desc_name']].set_index('fund_id').to_dict()['desc_name']
        self.fund_name_to_id = self.dts.fund_info[['fund_id', 'desc_name']].set_index('desc_name').to_dict()['fund_id']

    def get_fund_score(self, dt, index_id, is_filter_c) -> dict:
        assert self.params and self.dts, 'cannot provide fund_score without params or data tables'
        score, score_raw = self._get_score(index_id, dt, self.dts.index_fund_indicator_pack.loc[index_id, dt], is_filter_c)
        return score, score_raw

    def get_fund_scores(self, dt, index_list, is_filter_c=True) -> dict:
        if not self.score_cache:
            score = {}
            score_raw = {}
            for index_id in index_list:
                score[index_id], score_raw[index_id] = self.get_fund_score(dt, index_id, is_filter_c)
            return score, score_raw
        return self.score_cache.get(dt, {}), self.score_raw_cache.get(dt, {})

    def _wrapper(self, df: pd.DataFrame, is_filter_c: bool):
        # T日大类下有很多基金，这里取一下它们的datetime和index_id，因为值都是一样的所以取array[0]就OK
        dt = df.datetime.array[0]
        index_id: str = df.index_id.array[0]
        # 这里把index换成了fund_id
        score, score_raw = self._get_score(index_id, dt, df.set_index('fund_id').drop(columns=['datetime', 'index_id']), is_filter_c)
        self.score_cache[dt][index_id] = score
        self.score_raw_cache[dt][index_id] = score_raw

    def pre_calculate(self, is_filter_c=True):
        # self.dts.fund_indicator.pivot_table(index=['datetime', 'index_id'])
        # 上面这一行会耗时10秒左右，且之后遍历index(datetime-index_id pair)也会比下边groupby慢一些
        # 这里应该没必要先groupby datetime，再groupby index_id（如果真这样可能更慢吧）
        self.dts.fund_indicator.groupby(by=['datetime', 'index_id']).apply(lambda x: self._wrapper(x, is_filter_c))

    def _get_score(self, index_id, dt, cur_d, is_filter_c):
        fund_ids = self._filter_size_and_com_hold(dt, index_id, cur_d.index)
        if fund_ids is not cur_d.index:
            # 这里没有dropna总计可以快24秒
            cur_d = cur_d.reindex(fund_ids)
        if cur_d.shape[0] > 1:
            # 不做归一化
            # nd_array = cur_d[['alpha', 'fee_rate', 'track_err']].to_numpy()
            # nd_array_calc = (nd_array - nd_array.mean(axis=0) + 1e-6) / (nd_array.std(axis=0, ddof=1) + 1e-6)
            # nd_array_same = cur_d[['beta']].to_numpy()
            # indicator_ndarry = np.concatenate([nd_array_calc, nd_array_same], axis=1)
            indicator_ndarry = cur_d[['alpha', 'fee_rate', 'track_err', 'beta']].to_numpy()
            func = self.funcs.get(index_id)
            # TODO: could broadcast the func to do vectorize calc
            score_list = np.apply_along_axis(lambda x: func.get(x), 1, indicator_ndarry)
            score_raw = pd.Series(score_list, index=cur_d.index)
            if index_id in self.score_penalty_param.FilterYearIndex:
                punish_funds = cur_d[cur_d.year_length < self.score_penalty_param.JudgeYearLength].index.tolist()
                for _fund_id in punish_funds:
                    score_raw[_fund_id] += self.score_penalty_param.Penalty
                # 以下是vectorize calc, 但看起来没有明显的加速效果
                # punish_funds = pd.Series(self.score_penalty_param.Penalty, index=cur_d[cur_d.year_length < self.score_penalty_param.JudgeYearLength].index)
                # score_raw = score_raw.add(punish_funds, fill_value=0)
            score = (score_raw - score_raw.min()) / (score_raw.max() - score_raw.min())
            if is_filter_c:
                score = self._filter_score(score)
            score = score.to_dict()
            score_raw = score_raw.to_dict()
        else:
            score_raw = {cur_d.index[0]: 1}
            score = score_raw
        return score, score_raw

    def _filter_size_and_com_hold(self, dt, index_id: str, fund_ids: pd.Index):
        if index_id not in self.score_filter.FilterIndexId:
            return fund_ids

        try:
            # retrieve from cache
            _select_funds = self._size_and_com_hold_cache[dt]
        except KeyError:
            try:
                fund_com_hold_dt = self.dts.fund_com_hold.loc[dt]
            except KeyError:
                return fund_ids

            hold_select_fund_id = fund_com_hold_dt[fund_com_hold_dt < self.score_filter.CompanyHoldLimit].index
            fund_size_dt = self.dts.fund_size.loc[dt]
            size_select_fund_id = fund_size_dt[(fund_size_dt >= self.score_filter.SizeBottom)
                                               & (fund_size_dt <= self.score_filter.SizeTop)].index
            _select_funds = hold_select_fund_id.intersection(size_select_fund_id)
            # 这里做了一个缓存：T日备选的基金列表；因为多个大类可能多次取同一日的备选基金列表
            # 这个缓存没有清理，但看起来应该没问题
            self._size_and_com_hold_cache[dt] = _select_funds
        select_funds = _select_funds.intersection(fund_ids)
        if select_funds.empty:
            return fund_ids
        else:
            return select_funds

    def _filter_score(self, score_series: pd.Series) -> pd.Series:
        # 同一天同资产 同基金A B 在 选B
        # 同一天同资产 同基金A C 在 选C
        # 这里比之前总计快6秒左右
        index_fund_name: Set[str] = {self.fund_id_to_name[_] for _ in score_series.index}
        for fund_name in index_fund_name:
            if 'B' in fund_name or 'C' in fund_name:
                prefered_fund, count = re.subn(r'[BC]$', 'A', fund_name)
                if count != 0 and prefered_fund in index_fund_name:
                    score_series[self.fund_name_to_id[prefered_fund]] = 0
        return score_series

    def _white_and_black_list_filter(self, score, score_raw, disproved_set):
        score = self._white_black_func(score, disproved_set)
        score_raw = self._white_black_func(score_raw, disproved_set)
        return score, score_raw

    def _white_black_func(self, score, disproved_set):
        for index_id in score:
            for fund_id in score[index_id]:
                if fund_id in disproved_set:
                    score[index_id][fund_id] += self.score_penalty_param.BlackListPenalty
        return score

    @staticmethod
    def test_func(func_str):
        for item in ScoreFunc.__dataclass_fields__.keys():
            locals()[item] = 0
        # if we cannot calculate, it just breaks
        eval(func_str)
        return True

    @staticmethod
    def get_func(func_str):
        new_func = func_str
        for item in ScoreFunc.__dataclass_fields__.keys():
            new_func = new_func.replace(item, 'x.' + item)
        return lambda x: eval(new_func)

    @staticmethod
    def score_calc(func_str, dm, index_id, dt):
        cur_d = dm.dts.index_fund_indicator_pack.loc[index_id, dt]
        f = FundScoreManager.get_func(func_str)
        return cur_d.apply(f, axis=1)
