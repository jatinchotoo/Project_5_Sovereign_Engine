from dataclasses import dataclass
from typing import List, Dict


@dataclass
class StrategicSignal:
    name: str
    impact: float
    risk_level: str
    narrative: str


class SovereignEngine:
    def __init__(self):
        self.capital_base = 500_000_000
        self.hurdle_rate = 0.12

        self.signals: List[StrategicSignal] = [
            StrategicSignal(
                name="Macroeconomic Tightening",
                impact=-0.18,
                risk_level="High",
                narrative="Rising rates and liquidity contraction are pressuring valuation multiples."
            ),
            StrategicSignal(
                name="Core Business Resilience",
                impact=0.22,
                risk_level="Low",
                narrative="Recurring revenue streams demonstrate strong margin durability."
            ),
            StrategicSignal(
                name="Technology Leverage",
                impact=0.15,
                risk_level="Medium",
                narrative="Automation and analytics investments improve operating leverage over time."
            ),
            StrategicSignal(
                name="Geopolitical Exposure",
                impact=-0.10,
                risk_level="Medium",
                narrative="Regional concentration introduces tail-risk exposure."
            )
        ]

    def _weighted_signal_score(self) -> float:
        score = 0.0
        for signal in self.signals:
            score += signal.impact
        return score

    def _risk_adjustment_factor(self) -> float:
        high_risk = sum(1 for s in self.signals if s.risk_level == "High")
        medium_risk = sum(1 for s in self.signals if s.risk_level == "Medium")

        adjustment = 1.0 - (high_risk * 0.08) - (medium_risk * 0.04)
        return max(adjustment, 0.7)

    def capital_allocation_recommendation(self) -> Dict[str, float]:
        score = self._weighted_signal_score()
        risk_factor = self._risk_adjustment_factor()

        growth_allocation = self.capital_base * max(0.3 + score, 0.2) * risk_factor
        defensive_allocation = self.capital_base * 0.35
        liquidity_reserve = self.capital_base - (growth_allocation + defensive_allocation)

        return {
            "Growth Investment": round(growth_allocation, 2),
            "Defensive Capital": round(defensive_allocation, 2),
            "Liquidity Reserve": round(liquidity_reserve, 2)
        }

    def generate_advisory_report(self) -> str:
        score = self._weighted_signal_score()
        risk_factor = self._risk_adjustment_factor()
        allocation = self.capital_allocation_recommendation()

        lines = []
        lines.append("=" * 70)
        lines.append("SOVEREIGN ENGINE — STRATEGIC ADVISORY REPORT")
        lines.append("=" * 70)
        lines.append("")
        lines.append("EXECUTIVE CONTEXT:")
        lines.append(
            "This report synthesizes strategic signals to support capital allocation "
            "and executive decision-making under uncertainty."
        )
        lines.append("")

        lines.append("KEY STRATEGIC SIGNALS:")
        for s in self.signals:
            lines.append(f"- {s.name} | Risk: {s.risk_level}")
            lines.append(f"  {s.narrative}")

        lines.append("")
        lines.append(f"AGGREGATE STRATEGIC SCORE: {round(score, 2)}")
        lines.append(f"RISK ADJUSTMENT FACTOR: {round(risk_factor, 2)}")
        lines.append("")

        lines.append("CAPITAL ALLOCATION GUIDANCE:")
        for k, v in allocation.items():
            lines.append(f"- {k}: ${v:,.2f}")

        lines.append("")
        lines.append("ADVISORY CONCLUSION:")
        lines.append(
            "Maintain disciplined growth investment while preserving defensive buffers. "
            "Liquidity should be retained to exploit dislocations or mitigate downside risk."
        )
        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)


if __name__ == "__main__":
    engine = SovereignEngine()
    report = engine.generate_advisory_report()
    print(report)
    print()
    print("PROJECT 5 COMPLETE – STRATEGIC ADVISORY ENGINE READY")
    
