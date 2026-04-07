from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import hashlib
import math
import statistics
import networkx as nx


@dataclass
class PlantNode:
    node_id: str
    name: str
    district: str
    lat: float
    lon: float
    plant_type: str
    capacity_mw: float
    current_output_mw: float
    min_stable_mw: float = 0.0
    ramp_rate_mw_per_min: float = 0.0
    risk_index: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoadHub:
    node_id: str
    name: str
    district: str
    lat: float
    lon: float
    demand_mw: float
    criticality: float = 1.0
    meta: Dict[str, Any] = field(default_factory=dict)


class TeraqitGridProcessor:
    """
    Hybrid quantum-classical planning engine for wide-district grid analysis.

    Designed for:
    - district mapping
    - plant/load/corridor modeling
    - telemetry snapshots
    - contingency screening
    - hybrid optimization
    - digital-twin reporting

    Not designed for:
    - direct breaker control
    - dispatch write-back
    - substation actuation
    """

    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.snapshots: List[Dict[str, Any]] = []
        self._last_digest: Optional[str] = None

    # -------------------------------------------------
    # Graph construction
    # -------------------------------------------------
    def add_plant(self, plant: PlantNode) -> None:
        self.graph.add_node(
            plant.node_id,
            kind="plant",
            name=plant.name,
            district=plant.district,
            lat=plant.lat,
            lon=plant.lon,
            plant_type=plant.plant_type,
            capacity_mw=float(plant.capacity_mw),
            current_output_mw=float(plant.current_output_mw),
            min_stable_mw=float(plant.min_stable_mw),
            ramp_rate_mw_per_min=float(plant.ramp_rate_mw_per_min),
            risk_index=float(plant.risk_index),
            meta=dict(plant.meta),
        )

    def add_load_hub(self, hub: LoadHub) -> None:
        self.graph.add_node(
            hub.node_id,
            kind="load",
            name=hub.name,
            district=hub.district,
            lat=hub.lat,
            lon=hub.lon,
            demand_mw=float(hub.demand_mw),
            criticality=float(hub.criticality),
            meta=dict(hub.meta),
        )

    def add_transmission_corridor(
        self,
        src: str,
        dst: str,
        thermal_limit_mw: float,
        impedance_pu: float = 0.1,
        loss_factor: float = 0.02,
        reliability: float = 0.99,
    ) -> None:
        if src not in self.graph or dst not in self.graph:
            raise KeyError(f"Missing endpoint(s): {src}, {dst}")

        self.graph.add_edge(
            src,
            dst,
            thermal_limit_mw=float(thermal_limit_mw),
            impedance_pu=float(impedance_pu),
            loss_factor=float(loss_factor),
            reliability=float(reliability),
        )

    # -------------------------------------------------
    # Telemetry ingest
    # -------------------------------------------------
    def ingest_snapshot(self, timestamp: str, telemetry: Dict[str, Dict[str, float]]) -> str:
        """
        Example telemetry:
        {
            "plant_a": {"current_output_mw": 420.0, "risk_index": 0.08},
            "load_x": {"demand_mw": 315.0}
        }
        """
        changed_nodes = []

        for node_id, values in telemetry.items():
            if node_id not in self.graph:
                continue

            for key, value in values.items():
                self.graph.nodes[node_id][key] = float(value)

            changed_nodes.append(node_id)

        digest_source = {
            "timestamp": timestamp,
            "changed_nodes": sorted(changed_nodes),
            "telemetry": telemetry,
        }
        digest = hashlib.sha256(repr(digest_source).encode()).hexdigest()
        self._last_digest = digest
        self.snapshots.append({"timestamp": timestamp, "digest": digest})
        return digest

    # -------------------------------------------------
    # District + system metrics
    # -------------------------------------------------
    def district_balance(self) -> Dict[str, Dict[str, float]]:
        districts: Dict[str, Dict[str, float]] = {}

        for _, data in self.graph.nodes(data=True):
            district = data.get("district", "UNKNOWN")
            bucket = districts.setdefault(
                district,
                {"generation_mw": 0.0, "capacity_mw": 0.0, "load_mw": 0.0, "reserve_mw": 0.0}
            )

            if data["kind"] == "plant":
                bucket["generation_mw"] += data.get("current_output_mw", 0.0)
                bucket["capacity_mw"] += data.get("capacity_mw", 0.0)
            elif data["kind"] == "load":
                bucket["load_mw"] += data.get("demand_mw", 0.0)

        for district, bucket in districts.items():
            bucket["reserve_mw"] = bucket["generation_mw"] - bucket["load_mw"]

        return districts

    def system_metrics(self) -> Dict[str, float]:
        total_generation = 0.0
        total_capacity = 0.0
        total_load = 0.0
        plant_risks: List[float] = []
        edge_pressure: List[float] = []

        for _, data in self.graph.nodes(data=True):
            if data["kind"] == "plant":
                total_generation += data.get("current_output_mw", 0.0)
                total_capacity += data.get("capacity_mw", 0.0)
                plant_risks.append(data.get("risk_index", 0.0))
            else:
                total_load += data.get("demand_mw", 0.0)

        for _, _, edata in self.graph.edges(data=True):
            edge_pressure.append(1.0 - edata.get("reliability", 1.0))

        reserve_margin = (total_capacity - total_load) / total_load if total_load else 0.0
        generation_margin = (total_generation - total_load) / total_load if total_load else 0.0

        return {
            "total_generation_mw": total_generation,
            "total_capacity_mw": total_capacity,
            "total_load_mw": total_load,
            "reserve_margin_ratio": reserve_margin,
            "generation_margin_ratio": generation_margin,
            "avg_plant_risk": statistics.mean(plant_risks) if plant_risks else 0.0,
            "avg_edge_pressure": statistics.mean(edge_pressure) if edge_pressure else 0.0,
        }

    # -------------------------------------------------
    # Lightweight forecasting
    # -------------------------------------------------
    @staticmethod
    def exponential_forecast(series: List[float], alpha: float = 0.35, horizon: int = 6) -> List[float]:
        if not series:
            raise ValueError("series must contain at least one value")

        level = float(series[0])
        for value in series[1:]:
            level = alpha * float(value) + (1.0 - alpha) * level

        return [level for _ in range(horizon)]

    # -------------------------------------------------
    # Contingency screening
    # -------------------------------------------------
    def n_minus_one_screen(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        plant_nodes = [n for n, d in self.graph.nodes(data=True) if d["kind"] == "plant"]
        for node in plant_nodes:
            g = self.graph.copy()
            lost_output = g.nodes[node].get("current_output_mw", 0.0)
            g.remove_node(node)

            total_gen = sum(
                d.get("current_output_mw", 0.0)
                for _, d in g.nodes(data=True)
                if d["kind"] == "plant"
            )
            total_load = sum(
                d.get("demand_mw", 0.0)
                for _, d in g.nodes(data=True)
                if d["kind"] == "load"
            )
            unmet = max(0.0, total_load - total_gen)

            results.append({
                "type": "plant_outage",
                "target": node,
                "lost_output_mw": lost_output,
                "unmet_load_mw": unmet,
                "severity": lost_output + 2.0 * unmet,
            })

        for src, dst, edata in list(self.graph.edges(data=True)):
            g = self.graph.copy()
            g.remove_edge(src, dst)

            components = list(nx.connected_components(g))
            islands = len(components)
            penalty = 0.0

            if islands > 1:
                for comp in components:
                    island_gen = sum(
                        g.nodes[n].get("current_output_mw", 0.0)
                        for n in comp
                        if g.nodes[n]["kind"] == "plant"
                    )
                    island_load = sum(
                        g.nodes[n].get("demand_mw", 0.0)
                        for n in comp
                        if g.nodes[n]["kind"] == "load"
                    )
                    penalty += max(0.0, island_load - island_gen)

            results.append({
                "type": "corridor_outage",
                "target": f"{src}->{dst}",
                "thermal_limit_mw": edata.get("thermal_limit_mw", 0.0),
                "islands": islands,
                "unmet_load_mw": penalty,
                "severity": penalty + (1.0 - edata.get("reliability", 1.0)) * 100.0,
            })

        return sorted(results, key=lambda x: x["severity"], reverse=True)

    # -------------------------------------------------
    # Hybrid quantum-classical partitioning
    # -------------------------------------------------
    def _build_partition_graph(self) -> nx.Graph:
        g = nx.Graph()

        for node, data in self.graph.nodes(data=True):
            g.add_node(node, **data)

        for u, v, edata in self.graph.edges(data=True):
            weight = (
                float(edata.get("thermal_limit_mw", 0.0)) *
                float(edata.get("reliability", 1.0))
            ) / max(0.01, float(edata.get("impedance_pu", 0.1)))
            g.add_edge(u, v, weight=weight)

        return g

    @staticmethod
    def _cut_value(g: nx.Graph, group_a: set, group_b: set) -> float:
        cut = 0.0
        for u, v, edata in g.edges(data=True):
            if (u in group_a and v in group_b) or (u in group_b and v in group_a):
                cut += float(edata.get("weight", 1.0))
        return cut

    def _classical_partition(self) -> Dict[str, Any]:
        g = self._build_partition_graph()

        if g.number_of_nodes() < 2:
            return {"method": "classical", "group_a": list(g.nodes()), "group_b": [], "cut_value": 0.0}

        plants = [n for n, d in g.nodes(data=True) if d.get("kind") == "plant"]
        if plants:
            group_a = set(plants[: max(1, len(plants) // 2)])
            group_b = set(g.nodes()) - group_a
        else:
            nodes = list(g.nodes())
            group_a = set(nodes[: len(nodes) // 2])
            group_b = set(nodes[len(nodes) // 2:])

        improved = True
        while improved:
            improved = False
            current_cut = self._cut_value(g, group_a, group_b)

            for node in list(g.nodes()):
                a2 = set(group_a)
                b2 = set(group_b)

                if node in a2:
                    a2.remove(node)
                    b2.add(node)
                else:
                    b2.remove(node)
                    a2.add(node)

                new_cut = self._cut_value(g, a2, b2)
                if new_cut < current_cut:
                    group_a, group_b = a2, b2
                    current_cut = new_cut
                    improved = True

        return {
            "method": "classical",
            "group_a": sorted(group_a),
            "group_b": sorted(group_b),
            "cut_value": self._cut_value(g, group_a, group_b),
        }

    def _quantum_partition(self) -> Optional[Dict[str, Any]]:
        """
        Small bounded quantum subproblem.
        Uses Qiskit if available; otherwise returns None.
        Keeps the quantum portion intentionally small.
        """
        try:
            from qiskit import QuantumCircuit
            from qiskit.quantum_info import Statevector
        except Exception:
            return None

        g = self._build_partition_graph()
        nodes = list(g.nodes())
        n = len(nodes)

        if n == 0:
            return {"method": "quantum", "group_a": [], "group_b": [], "cut_value": 0.0}

        if n > 8:
            return None  # bounded subproblem only

        qc = QuantumCircuit(n)
        for i in range(n):
            qc.h(i)

        index = {node: idx for idx, node in enumerate(nodes)}

        for u, v, edata in g.edges(data=True):
            w = max(0.01, float(edata.get("weight", 1.0)))
            theta = min(math.pi / 4.0, 0.002 * w)

            iu, iv = index[u], index[v]
            qc.cx(iu, iv)
            qc.rz(theta, iv)
            qc.cx(iu, iv)

        state = Statevector.from_instruction(qc)
        probs = state.probabilities_dict()
        best_bitstring = max(probs.items(), key=lambda item: item[1])[0][::-1]

        group_a = [nodes[i] for i, bit in enumerate(best_bitstring) if bit == "0"]
        group_b = [nodes[i] for i, bit in enumerate(best_bitstring) if bit == "1"]

        return {
            "method": "quantum",
            "group_a": sorted(group_a),
            "group_b": sorted(group_b),
            "cut_value": self._cut_value(g, set(group_a), set(group_b)),
            "state_probability": float(max(probs.values())),
        }

    def optimize_partition(self) -> Dict[str, Any]:
        quantum = self._quantum_partition()
        if quantum is not None:
            return quantum
        return self._classical_partition()

    # -------------------------------------------------
    # Wide-district map payload
    # -------------------------------------------------
    def wide_district_map(self) -> Dict[str, Any]:
        nodes = []
        edges = []

        for node_id, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node_id,
                "name": data.get("name"),
                "kind": data.get("kind"),
                "district": data.get("district"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "capacity_mw": data.get("capacity_mw"),
                "current_output_mw": data.get("current_output_mw"),
                "demand_mw": data.get("demand_mw"),
            })

        for src, dst, edata in self.graph.edges(data=True):
            s = self.graph.nodes[src]
            d = self.graph.nodes[dst]
            edges.append({
                "src": src,
                "dst": dst,
                "src_lat": s.get("lat"),
                "src_lon": s.get("lon"),
                "dst_lat": d.get("lat
